import numpy as np
import cmath
import math
def DFT(data):
    # lFrame_ = len(data)  # frame length lFram = 2.Ls in publication
    # t = 0
    # for n_ in range(lFrame_):
    #     t += data[n_] * cmath.exp(-2 * math.pi * 1j * m * n_ / (lFrame_ - 1))
    # return t
    fourierTransform = np.fft.fft((data) / len(data))
    return (fourierTransform)

def entropyDFT(dftData):
    p_ = dftData / np.sum(dftData[1:])
    return p_

def getDFT(data):
    x_ = [] # Empty vector
    lengFrame = len(data)
    absDFTData_ = np.empty((lengFrame))  # matrix containing DFT data from input data
    absDFTData_[:] = np.NaN
    for i in range(lengFrame):
        absDFTData_ = np.absolute(DFT(data))
            # Add DC component as features (for each axis x,y,z)
    x_.append(absDFTData_[0])

        # Add energy features (exclude DC component)
    x_.append((np.sum(np.power(absDFTData_[1:], 2), axis=0) / (lengFrame - 1)))

        # Add entropy features (exclude DC component)
    entropyDFTData_ = np.empty((lengFrame))
    entropyDFTData_[:] = np.NaN
    entropyDFTData_ = entropyDFT(absDFTData_)
    x_.append(np.sum(entropyDFTData_[1:] * np.log(1 / entropyDFTData_[1:]), axis=0))

        # Add deviation features (time domain)
    datMean = np.mean(data, axis=0)
    x_.append(np.sum(np.power(data - datMean, 2), axis=0))

    return(x_)