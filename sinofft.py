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

startTime = datetime.now()

head = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.5]), radius=0.5))
head.mass_atten = 3.0

#circleL = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.3,0.5]), radius=0.01))
#circleL.mass_atten = -100.0

circleR = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.7,0.5]), radius=0.2))
circleR.mass_atten = -3.0

#head.append(circleL)
head.append(circleR)

head.sprinkle(5, radius=0.01, mass_atten = -100)

# Create sinogram
sx = 200
sy = 200
sino, prb = xdesign.sinogram(sx, sy, head, noise = 0)
sino = np.reshape(sino, (sx, sy))


# Add misalignment using numpy roll
#sino[100,:] = np.roll(sino[100,:], 15)
#sino[200,:] = np.roll(sino[200,:], -15)
#sino[300,:] = np.roll(sino[300,:], -15)
#sino[400,:] = np.roll(sino[400,:], 15)
#sino[450,:] = np.roll(sino[450,:], 15)

#sino_ref = np.fliplr(sino)
zeros = np.zeros((sx,sy))
sino1 = copy.deepcopy(sino)

# Add misalignment

#misalign_by = 4
#y = set(range(-misalign_by,misalign_by+1))
#for k in range(sx):
#    ds = random.sample(y, 1)
#    sino1[k,:] = np.roll(sino1[k,:], ds)

# Construct a full wave from the half wave
x = np.concatenate((zeros,sino1),axis=0)
sino_full = x + np.flipud(x)

# Take fast fourier transform of the full wave
sino_fft = np.abs(fft.fftshift(fft.fft2(sino_full)))


dnp.plot.image(sino_fft, name="sino_fft2")
dnp.plot.image(sino_full, name="sino")

print datetime.now() - startTime