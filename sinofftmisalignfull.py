#Create Phantom
import numpy as np
import xdesign
import copy
import random
 
circle_phantom = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.6,0.5]),radius=0.1))
circle_phantom.mass_atten = 3.0
circle = xdesign.plot.discrete_phantom(circle_phantom, size=200)
 
#Can use any plotting tool to plot an array as an image
import scisoftpy as dnp
import matplotlib.pyplot as plt

#Create Sinogram
sx = 200
sy = 400
sino_circle, prb = xdesign.sinogram(sx, sy, circle_phantom, noise = 0.5)
sino_circle = np.reshape(sino_circle, (sx, sy))

#Add misalignment
misalign = 5
sino1 = copy.deepcopy(sino_circle)
y = set(range(-misalign,misalign+1))
for k in range(sx):
    ds = random.sample(y, 1)
    sino1[k,:] = np.roll(sino1[k,:], ds)

#Create full wave
zeros = np.zeros(sino1.shape)
x = np.concatenate((zeros,sino1),axis=0)
sino_circle_full = x + np.flipud(x)

plt.figure(1)
color = 'viridis'
plt.subplot(121)
#dnp.plot.image(sino_circle_full, name="Sinogram of circle")
one = plt.imshow(sino_circle_full)
one.set_cmap(color)
 
#Take Fourier Transform of Sinogram
import pyfftw.interfaces.scipy_fftpack as fft
 
sino_circle_fft = np.abs(fft.fftshift(fft.fft2(sino_circle_full)))
#dnp.plot.image(sino_circle_fft, name="FFT of Circle Sinogram")
plt.subplot(122)
sino_circle_fft_plot = sino_circle_fft[...]
sino_circle_fft_plot[sino_circle_fft_plot>1] = 1
two = plt.imshow(sino_circle_fft_plot)
two.set_cmap(color)

plt.savefig('/scratch/U_ytp88384/pictures/misalignfullnoise.png', dpi=300)
plt.show()