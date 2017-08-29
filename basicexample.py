#Create Phantom
import numpy as np
import xdesign
 
circle_phantom = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.6,0.5]), radius=0.1))
circle_phantom.mass_atten = 3.0
circle = xdesign.plot.discrete_phantom(circle_phantom, size=200)
 
#Can use any plotting tool to plot an array as an image
import scisoftpy as dnp
dnp.plot.image(circle, name="Circle phantom")
 
#Create Sinogram
sx = 200
sy = 200
sino_circle, prb = xdesign.sinogram(sx, sy, circle_phantom)
sino_circle = np.reshape(sino_circle, (sx, sy))
 
dnp.plot.image(sino_circle, name="Sinogram of circle")
 
#Take Fourier Transform of Sinogram
import pyfftw.interfaces.scipy_fftpack as fft
 
sino_circle_fft = np.abs(fft.fftshift(fft.fft2(sino_circle)))
dnp.plot.image(sino_circle_fft, name="FFT of Circle Sinogram")