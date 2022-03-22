import pandas as pd
import numpy as np
import seaborn as sns
import staticFeatures
import kinematicFeatures
import tiltFeatures

#In order to calculate the orientation of the written text, we define how much the entire dataset should be split
#for each split, we take the (x,y) value and calculate the direction vector.
#The vector will be the reference direction to calculate e.g. how much variance is there around this direction?
#Note: The vector is calculated in an area around the window, not only for the window
#The directionSize defines how many data points should be taken around the middle data point of the window

directionSize= 50

def handwritingMoment():
    return 0

#window = dataframe consisting of tip, top accX,Y,Z; tilt-azimuth, tilt-altitude
#indStart = Starting index
#windowSize = window size parameter
#data = whole dataframe (useful for relative calculations)

def createFeatures(window, indStart, windowSize, data):

    tiltDataFrame = tiltFeatures.tiltFeatures(window)

    kinematicDataFrame = kinematicFeatures.kinematicFeatures(window)
    #staticDataFrame = staticFeatures.staticFeatures(window)
    #featuresByWindowDF = pd.concat([tiltDataFrame,kinematicDataFrame,staticDataFrame],axis=1)
    # featuresByWindowDF = tiltDataFrame

    featuresByWindowDF = pd.concat([tiltDataFrame, kinematicDataFrame], axis=1, join="inner")

    # print('HERE')
    # print(tiltDataFrame.head(5))
    # print(kinematicDataFrame.head(5))
    # print(featuresByWindowDF.head(5))

    return featuresByWindowDF