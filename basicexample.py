#Create Phantom
import numpy as np
import xdesign
import matplotlib.pyplot as plt
from datetime import datetime

startTime = datetime.now()

plt.figure(1)

head = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.5]), radius=0.5))
head.mass_atten = 0

circle_phantom1 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.2,0.2]), radius=0.05))
circle_phantom1.mass_atten = 4.0

circle_phantom2 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.75,0.75]), radius=0.1))
circle_phantom2.mass_atten = 4.0

#mouth = xdesign.Phantom(geometry=xdesign.Triangle(xdesign.Point([0.2, 0.7]), xdesign.Point([0.5, 0.8]), xdesign.Point([0.8, 0.7])))
#mouth.mass_atten = -2.0

head.append(circle_phantom1)
head.append(circle_phantom2)
#head.append(mouth)
circle = xdesign.plot.discrete_phantom(head, size=200)
 
#Can use any plotting tool to plot an array as an image
#import scisoftpy as dnp
#dnp.plot.image(circle, name="Circle phantom")
color = 'viridis'
plt.subplot(141)
one = plt.imshow(circle)
one.set_cmap(color)

#Create Sinogram
sx = 400
sy = 400
sino_circle, prb = xdesign.sinogram(sx, sy, head)
sino_circle = np.reshape(sino_circle, (sx, sy))
 
#dnp.plot.image(sino_circle, name="Sinogram of circle")
plt.subplot(142)
two = plt.imshow(sino_circle)
two.set_cmap(color)

#Take Fourier Transform of Sinogram
import pyfftw.interfaces.scipy_fftpack as fft
 
sino_circle_fft = np.abs(fft.fftshift(fft.fft2(sino_circle)))
#dnp.plot.image(sino_circle_fft, name="FFT of Circle Sinogram")
plt.subplot(143)
sino_circle_fft_plot = sino_circle_fft[...]
sino_circle_fft_plot[sino_circle_fft_plot>2.1] = 2.1
#sino_circle_fft_plot[sino_circle_fft_plot<0.5] = 0.5
three = plt.imshow(sino_circle_fft_plot)
three.set_cmap(color)

zeros = np.zeros(sino_circle.shape)
x = np.concatenate((zeros,sino_circle),axis=0)
sino_circle_full = x + np.flipud(x)

sino_circle_full_fft = np.abs(fft.fftshift(fft.fft2(sino_circle_full)))
plt.subplot(144)
sino_circle_full_fft_plot = sino_circle_full_fft[...]
sino_circle_full_fft_plot[sino_circle_full_fft_plot>2.1] = 2.1
l = sino_circle_full_fft_plot.shape[0]
four = plt.imshow(sino_circle_full_fft_plot[int(l*0.25):int(l*0.75),:])
four.set_cmap(color)

print datetime.now() - startTime
#plt.figure(2)
#plt.hist(sino_circle_full_fft)
#plt.savefig('/scratch/Shahzaib/basicexample.jpg', dpi=300)
plt.show()
