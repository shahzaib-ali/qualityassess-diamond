from datetime import datetime

startTime = datetime.now()

import numpy as np
import pyfftw.interfaces.scipy_fftpack as fft
import scisoftpy as dnp
import mrcfile as mrc
import h5py

def imagequality(filename1, filename2):
    raw_file1 = mrc.open(filename1)
    raw_data1 = np.array(raw_file1.data)
    raw_file1.close()
    
    raw_file2 = mrc.open(filename2)
    raw_data2 = np.array(raw_file2.data)
    raw_file2.close()
    
    sinos1, sino_fft1, quality1 = quality(raw_data1)
    sinos2, sino_fft2, quality2 = quality(raw_data2)

    #dnp.plot.line([quality1, quality2], name="qualitycompare")
    return quality1, sinos1, sino_fft1, quality2, sinos2, sino_fft2

def quality(data):
    """Calculate quality value from different sinograms in the data
    
    Usage::
    
    :param data
    :rtype
    """
    pass
    # Extract sinogram
    sinos = picksino(data)
    # Create full sinogram
    sino_full = reflectsinos(sinos)
    # Apply fft
    sino_fft = applyfft(sino_full)
    # Extract middle vertical slice and calculate quality value
    fftquality = fft_quality(sino_fft)
    # Output sino, sino_fft and quality value
    return sinos, sino_fft, fftquality
    
def fft_array_quality(fftarray):
    angle = fftarray.shape[0]
    angle11 = int(angle*0.3)
    angle12 = int(angle*0.4)
    angle21 = int(angle*0.6)
    angle22 = int(angle*0.7)
    x = fftarray.shape[1]
    x1 = int(x*0.45)
    x2 = int(x*0.55)
    vert_strip_up = fftarray[:angle12, x1:x2]
    vert_strip_down = fftarray[angle21:, x1:x2]
    sum_intens = vert_strip_up.sum() + vert_strip_down.sum()
    ratio = sum_intens/fftarray.sum()
    return ratio

def fft_quality(sino_fft):
    fftquality = []
    for n in range(sino_fft.shape[1]):
        fftquality.append(fft_array_quality(sino_fft[:,n,:]))
    return fftquality

def picksino(image):
    yrange = image.shape[1]
    gap = int(yrange/100)
    #sinos = image[:,::gap,:]
    sinos = (image[:,:-2:gap,:]+image[:,1:-1:gap,:]+image[:,2::gap,:])/3.0
    #sinos = (image[:,:-3:gap,:]+image[:,1:-2:gap,:]+image[:,2:-1:gap,:]+image[:,3::gap,:])/4.0
    return sinos

def reflectsinos(sinos):
    zeros1 = np.zeros(sinos[:,0,:].shape)
    zeros2 = np.zeros(sinos.shape)
    num = sinos.shape[1]
    sino_full = np.concatenate((zeros2,zeros2),axis=0)
    for n in range(num):
        x = np.concatenate((zeros1,sinos[:,n,:]),axis=0)
        sino_full[:,n,:] = x + np.flipud(x)
    return sino_full

def applyfft(sinos):
    sino_fft = np.zeros(sinos.shape)
    num = sinos.shape[1]
    for n in range(num):
        sino_fft[:,n,:] = np.abs(fft.fftshift(fft.fft2(sinos[:,n,:])))
    return sino_fft

def qualitysavefile(file1,file2,output):
    q1, s1, sfft1, q2, s2, sfft2 = imagequality(file1, file2)
    result = h5py.File(output, "w")
    result.create_dataset("rawsino", data=s1)
    result.create_dataset("rawsinofft", data=sfft1)
    result.create_dataset("rawsinoquality", data=q1)
    result.create_dataset("alignsino", data=s2)
    result.create_dataset("alignsinofft", data=sfft2)
    result.create_dataset("alignsinoquality", data=q2)
    result.close()
    return 'done'

if __name__ == "__main__":
    file1 = "/scratch/test_shahzaib/MicheleB24/15_square8ts1_tomo_60t60_p5d_1s_mb1_Export.st"
    file2 = "/scratch/test_shahzaib/MicheleB24/15_square8ts1_tomo_60t60_p5d_1s_mb1_Export.ali"
    output = "/scratch/test_shahzaib/casestudies/NE6E100.hdf5"
    #qualitysavefile(file1, file2, output)
    
    q1, s1, sfft1, q2, s2, sfft2 = imagequality(file1, file2)
    s1grad = np.gradient(s1, axis=2)
    s2grad = np.gradient(s2, axis=2)
    import scipy.stats
    print scipy.stats.iqr(s1grad)
    print scipy.stats.iqr(s2grad)
    #dnp.plot.line(s1grad, name="sino1grad")
    #dnp.plot.line(s2grad, name="sino2grad")
    """
    #file1 = "/scratch/test_shahzaib/cryomarkerauto/cryo.st"
    #file2 = "/scratch/test_shahzaib/cryomarkerauto/cryo_fin.mrc"
    
    q1, s1, sfft1, q2, s2, sfft2 = imagequality(file1, file2)
    dnp.plot.line(dnp.array(q2)-dnp.array(q1), name="diff")
    #dnp.plot.line(dnp.array(q2), name="aligned")08_A1S2T1_65t70_p5_1s_mb1_Export
    #print np.mean(dnp.array(q2)-dnp.array(q1))
    #print np.std(dnp.array(q2)-dnp.array(q1))
    #dnp.plot.image(s1[:,70,:], name="sinoraw")
    #dnp.plot.image(s2[:,70,:], name="sinoalign")
    """
    print datetime.now() - startTime