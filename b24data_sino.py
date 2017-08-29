import mrcfile as mrc
import numpy as np
import pyfftw.interfaces.scipy_fftpack as fft
import scisoftpy as dnp
import copy

def fft_plot(fiename, name):
    raw_file = mrc.open(fiename)
    raw_data = np.array(raw_file.data)
    #import quality
    #quality.picksino(raw_file.data, name=name)
    raw_sino = raw_file.data[:,340:344:1,:].mean(1)
    #Try to take mirror image of the sinograms
    #This makes our fft a bit cleaner
    zeros = np.zeros(raw_sino.shape)
    sino1 = copy.deepcopy(raw_sino)
    x = np.concatenate((zeros,sino1),axis=0)
    sino_full = x + np.flipud(x)
    dnp.plot.image(sino_full, name=name+"_sino")
    raw_fft = np.abs(fft.fftshift(fft.fft2(sino_full)))
    dnp.plot.image(raw_fft, name=name+"_fft")
    raw_file.close()
    import quality
    sinos = quality.picksino(raw_data)
    print quality.applyfft(sinos).shape
    #dnp.plot.image(sinos[:,1,:], name = "sino")
    dnp.plot.image(quality.applyfft(sinos)[:,1,:], name = "sino_fft")
    return raw_fft
#fft_raw = fft_plot("/scratch/test_shahzaib/MicheleB24/15_square8ts1_tomo_60t60_p5d_1s_mb1_Export.st", "raw")
#fft_align = fft_plot("/scratch/test_shahzaib/MicheleB24/15_square8ts1_tomo_60t60_p5d_1s_mb1_Export.ali", "align")
fft_raw = fft_plot("/scratch/test_shahzaib/MicheleB24/83_square7ts3_tomo_60t60_p5d_1s_mb1_Export.st", "raw")
fft_align = fft_plot("/scratch/test_shahzaib/MicheleB24/83_square7ts3_tomo_60t60_p5d_1s_mb1_Export.ali", "align")

import quality

print fft_raw.shape
print quality.fft_quality(fft_raw)
print quality.fft_quality(fft_align) 
"""
raw_file = mrc.open("/scratch/test_shahzaib/MicheleB24/15_square8ts1_tomo_60t60_p5d_1s_mb1_Export.st")
data = np.array(raw_file.data)
print data.shape
raw_sino = data[:,457:460:1,:].mean(1)


dnp.plot.image(raw_sino, name="raw_sino")
raw_fft = np.abs(fft.fftshift(fft.fft2(raw_sino)))
dnp.plot.image(raw_fft, name="raw_fft")
raw_file.close()


dnp.plot.image(data[100,:,:], name="raw_tilt")
"""