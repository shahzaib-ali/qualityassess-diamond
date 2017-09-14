#Create Phantom
import numpy as np
import xdesign
import matplotlib.pyplot as plt
import scisoftpy as dnp
from datetime import datetime
from skimage.transform import radon

startTime = datetime.now()

plt.figure(1)

head = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.5]), radius=0.48))
head.mass_atten = 7.0

circle_phantom1 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.5]), radius=0.42))
circle_phantom1.mass_atten = 6.0

circle_phantom2 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.25]), radius=0.15))
circle_phantom2.mass_atten = 8.0

circle_phantom3 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.65,0.5]), radius=0.1))
circle_phantom3.mass_atten = -8.0

circle_phantom4 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.3,0.5]), radius=0.15))
circle_phantom4.mass_atten = -8.0

circle_phantom5 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.6]), radius=0.02))
circle_phantom5.mass_atten = 7.0

#mouth = xdesign.Phantom(geometry=xdesign.Triangle(xdesign.Point([0.2, 0.7]), xdesign.Point([0.5, 0.8]), xdesign.Point([0.8, 0.7])))
#mouth.mass_atten = -2.0

head.append(circle_phantom1)
head.append(circle_phantom2)
head.append(circle_phantom3)
head.append(circle_phantom4)
head.append(circle_phantom5)
#head.append(mouth)
circle = xdesign.plot.discrete_phantom(head, size=500)
 
#Can use any plotting tool to plot an array as an image
#import scisoftpy as dnp
dnp.plot.image(circle, name="Circle phantom")
#color = 'gray'
#plt.subplot(141)
#one = plt.imshow(circle)
#one.set_cmap(color)
"""
#Create Sinogram
sx = 500
sy = 500
sino_circle, prb = xdesign.sinogram(sx, sy, head)
sino_circle = np.reshape(sino_circle, (sx, sy))
 
dnp.plot.image(sino_circle, name="Sinogram of circle")
#plt.subplot(142)
#two = plt.imshow(sino_circle)
#two.set_cmap(color)
"""
theta = np.linspace(0., 180., max(circle.shape), endpoint=False)
sino_circle = radon(circle,theta=theta, circle=True)

dnp.plot.image(np.transpose(sino_circle), name="Sinogram of circle")
mirror_sino = np.flipud(sino_circle)
#mirror_sino = radon(mirror,theta=theta, circle=True)
sino_circle_full = np.concatenate((mirror_sino,sino_circle),axis=1)
dnp.plot.image(np.transpose(sino_circle_full), name="full")

#Take Fourier Transform of Sinogram
import pyfftw.interfaces.scipy_fftpack as fft


sino_circle_fft = np.abs(fft.fftshift(fft.fft2(sino_circle)))
#print sino_circle_fft
#dnp.plot.image(sino_circle_fft, name="FFT of Circle Sinogram")
#plt.subplot(143)
#sino_circle_fft_plot = sino_circle_fft[...]
#sino_circle_fft_plot[sino_circle_fft_plot>3] = 3
#sino_circle_fft_plot[sino_circle_fft_plot<0.5] = 0.5
#three = plt.imshow(sino_circle_fft_plot)
#three.set_cmap(color)

#zeros = np.zeros(sino_circle.shape)
#x = np.concatenate((zeros,sino_circle),axis=0)
#sino_circle_full = x + np.flipud(x)

#theta_full = np.linspace(0., 360., 2*max(circle.shape), endpoint=False)
#sino_circle_full = radon(circle,theta=theta_full, circle=True)
sino_circle_full_fft = np.abs(fft.fftshift(fft.fft2(sino_circle_full)))
#plt.subplot(144)
#sino_circle_full_fft_plot = sino_circle_full_fft[...]
#sino_circle_full_fft_plot[sino_circle_full_fft_plot>3] = 3
dnp.plot.image(np.transpose(sino_circle_full_fft), name="FFT of Circle Sinogram")
#l = sino_circle_full_fft_plot.shape[0]
#four = plt.imshow(sino_circle_full_fft_plot[int(l*0.25):int(l*0.75),:])
#four.set_cmap(color)

print datetime.now() - startTime
#plt.figure(2)
#plt.hist(sino_circle_full_fft)
#plt.savefig('/scratch/Shahzaib/basicexample.jpg', dpi=300)
#plt.show()
