'''
Created on 20 Jul 2017

@author: ytp88384
'''

import mrcfile as mrc
import numpy as np
import pyfftw.interfaces.scipy_fftpack as fft
import scisoftpy as dnp

def fft_plot(fiename, name):
    raw_file = mrc.open(fiename)
    raw_sino = raw_file.data[:,457:460:1,:].mean(1)
    dnp.plot.image(raw_sino, name=name+"_sino")
    raw_fft = np.abs(fft.fftshift(fft.fft2(raw_sino)))
    dnp.plot.image(raw_fft, name=name+"_fft")
    raw_file.close()
    return raw_fft

fft_raw = fft_plot("/scratch/test_shahzaib/cryo/cryo.st", "raw")
fft_align = fft_plot("/scratch/test_shahzaib/cryo/cryo.ali", "align")

dnp.plot.image(fft_raw-fft_align, name="diff_fft")