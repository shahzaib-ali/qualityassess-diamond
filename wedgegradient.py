import numpy as np
import xdesign
import scisoftpy as dnp
from skimage.transform import radon

circleradius = 0.05
head = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.5,0.5]), radius=0.48))
head.mass_atten = .0
circle_phantom1 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.6,0.4]),radius=circleradius))
circle_phantom1.mass_atten = -3.0
circle_phantom2 = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.7,0.7]), radius=circleradius/2))
circle_phantom2.mass_atten = -3.0

head.append(circle_phantom1)
head.append(circle_phantom2)

sy = 500
circle = xdesign.plot.discrete_phantom(head, size=sy)
dnp.plot.image(np.transpose(circle), name="Image")

theta = np.linspace(0., 180., max(circle.shape), endpoint=True)
sino_circle = radon(circle,theta=theta, circle=True)

mirror_sino = np.flipud(sino_circle)
sino_circle_full = np.concatenate((mirror_sino,sino_circle),axis=1)

dnp.plot.image(np.transpose(sino_circle_full), name="Sinogram")

import pyfftw.interfaces.scipy_fftpack as fft
 
sino_circle_fft = np.abs(fft.fftshift(fft.fft2(sino_circle_full)))
dnp.plot.image(np.transpose(sino_circle_fft), name="FFT of Sinogram")