import quality
import matplotlib.pyplot as plt
import numpy as np
import xdesign
 
circle_phantom = xdesign.Phantom(geometry=xdesign.Circle(xdesign.Point([0.6,0.5]), radius=0.1))
circle_phantom.mass_atten = 3.0
circle = xdesign.plot.discrete_phantom(circle_phantom, size=200)

plt.figure(1)
plt.subplot(141)
plt.imshow(circle)

