#Create Phantom
import numpy as np
import xdesign
from skimage.transform import radon
 
circle_phantom = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.75,0.75]),radius=0.01))
circle_phantom.mass_atten = -8.0
sy = 500
circle = xdesign.plot.discrete_phantom(circle_phantom, size=sy)
 
#Can use any plotting tool to plot an array as an image
import scisoftpy as dnp
#import matplotlib.pyplot as plt

#Create Sinogram
#sx = 200
#sy = 500
#sino_circle, prb = xdesign.sinogram(sx, sy, circle_phantom, noise = 0.0)
#sino_circle = np.reshape(sino_circle, (sx, sy))

theta = np.linspace(0., 180., max(circle.shape), endpoint=False)
sino_circle = radon(circle,theta=theta, circle=True)

#Add misalignment
#sino_circle[:,sy/4] = np.roll(sino_circle[:,sy/4], sy/50)

#Create full wave
#zeros = np.zeros(sino_circle.shape)
#x = np.concatenate((zeros,sino_circle),axis=0)
#sino_circle_full = x + np.flipud(x)

mirror_sino = np.flipud(sino_circle)
sino_circle_full = np.concatenate((mirror_sino,sino_circle),axis=1)

#plt.figure(1)
#color = 'gray'
#plt.subplot(121)
dnp.plot.image(np.transpose(sino_circle_full), name="Sinogram of circle")
#one = plt.imshow(sino_circle_full)
#one.set_cmap(color)
 
#Take Fourier Transform of Sinogram
import pyfftw.interfaces.scipy_fftpack as fft
 
sino_circle_fft = np.abs(fft.fftshift(fft.fft2(sino_circle_full)))
dnp.plot.image(np.transpose(sino_circle_fft), name="FFT of Circle Sinogram")
#plt.subplot(122)
#sino_circle_fft_plot = sino_circle_fft[...]
#sino_circle_fft_plot[sino_circle_fft_plot>1.5] = 1.5
#two = plt.imshow(sino_circle_fft)
#two.set_cmap(color)

#plt.savefig('/scratch/U_ytp88384/pictures/basicmisalign.png', dpi=300)
#plt.show()