'''
Created on 21 Jul 2017

@author: Shahzaib Ali
'''

import numpy as np
import scisoftpy as dnp
import pyfftw.interfaces.scipy_fftpack as fft
import xdesign
import copy
import random
from datetime import datetime
import matplotlib.pyplot as plt

startTime = datetime.now()

head = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.5]), radius=0.5))
head.mass_atten = 0

circleL = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.3,0.5]), radius=0.1))
circleL.mass_atten = 8.0

circleR = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.7,0.5]), radius=0.2))
circleR.mass_atten = 8.0

head.append(circleL)
head.append(circleR)

# Create sinogram
sx = 200
sy = 200
sino, prb = xdesign.sinogram(sx, sy, head, noise = 0.05)
sino = np.reshape(sino, (sx, sy))

headarray = xdesign.plot.discrete_phantom(head, sx)
print headarray.shape
dnp.plot.image(headarray, name="phantom")

# Calculate intensity of the vertical strip
def calc_intens(sino_fft):
    #vert_strip_up = sino_fft[80:120,:150]
    vert_strip_up = sino_fft[:150,80:120]
    #vert_strip_down = sino_fft[80:120,250:]
    vert_strip_down = sino_fft[250:,80:120]
    sum_intens = vert_strip_up.sum() + vert_strip_down.sum()
    # Take the ratio of the sum of slice in the array against the total sum of the array
    # This accounts for changing total sums
    ratio = sum_intens/sino_fft.sum()
    return ratio

def calc_fft(sino, misalign=4, sx=200):
    zeros = np.zeros((sx,sx))
    # Deep copy preserves sino array
    sino1 = copy.deepcopy(sino)
    
    # Add misalignment
    y = set(range(-misalign,misalign+1))
    for k in range(sx):
        ds = random.sample(y, 1)
        sino1[k,:] = np.roll(sino1[k,:], ds)
    
    # Construct a full wave from the half wave
    x = np.concatenate((zeros,sino1),axis=0)
    sino_full = x + np.flipud(x)
    
    # Take fast fourier transform of the full wave
    sino_fft = np.abs(fft.fftshift(fft.fft2(sino1)))
    
    intens = calc_intens(sino_fft)
    
    return intens

intense = []
for x in range(0,21):
    average = 0.0
    for num in range(3):
        average += calc_fft(sino, misalign=x, sx=sx)
    average = average/3
    intense.append(average)
print intense
#dnp.plot.addline(x=range(0,10), y=intense, title='Intensity against magnitude of misalignment', name='fft_misalign')
#dnp.plot.line(dnp.array(intense),title = 'Intensity of vertical line against misalignment magnitude', name = 'fft_misalign')
plt.figure(1)
plt.plot(intense)
plt.xlabel('Magnitude of misalignment')
plt.ylabel('Quality Value')
plt.title('Quality against misalignment magnitude')
print datetime.now() - startTime
plt.show()