import numpy as np
import math
import GetDFT
import createFeatures

X = []

def passThroughWindow(data, isRaw, dataWindow):

    X_ = []
    targetcount = 0
    lenDat_ = len(data)
    i = 0

    # Window rolling
    while i < (lenDat_ - 1):
        indStart_ = i
        indStop_ = indStart_ + dataWindow
        if (indStop_ >= lenDat_):
            indStop_ = lenDat_ - 1
        if (indStop_ - indStart_ >= 1):

            # Create window of raw data and pass it to the feature creator
            window = data[indStart_:indStop_]

            if(isRaw == False):
                createdFeatures = createFeatures.createFeatures(window,indStart_, dataWindow, data)

            if (isRaw ==True):
                # Get Fourier Features By window

                norme = data['norme']
                X_ = GetDFT.getDFT(norme[indStart_:indStop_])


                getFeaturesWindows(data, X_)

            targetcount += 1

            #We define a rolling window that overlapps with the old window by half
            i += math.floor(dataWindow / 2.0)


def getFeaturesWindows(data, X_):

    print('activate')
    Xtemp = []
    i = 0
    targetcount = 0



        # Create and fill Xtemp (Features Vector)
    if Xtemp == []:
        Xtemp = [X_]  # generate data set matrix
    else:
        Xtemp = np.append(Xtemp, [X_], axis=0)  # update data set matrix
    if np.where(np.isnan(Xtemp))[0].size > 0:
        print('break')
        # break

    # Empty Vector
    if len(Xtemp[:]) > 100000:
        if X == []:
            X = Xtemp
            Xtemp = []
        else:
            X = np.append(X, Xtemp, axis=0)
            Xtemp = []

    # # Get Categories (1/0)
    # if out == 1:
    #     Y = np.ones(targetcount)
    # if out == 0:
    #     Y = np.zeros(targetcount)
    # return (Xtemp,Y, window)








