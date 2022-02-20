import numpy as np
import seaborn as sns

#In order to calculate the orientation of the written text, we define how much the entire dataset should be split
#for each split, we take the (x,y) value and calculate the direction vector.
#The vector will be the reference direction to calculate e.g. how much variance is there around this direction?
#Note: The vector is calculated in an area around the window, not only for the window
#The directionSize defines how many data points should be taken around the middle data point of the window

directionSize= 50

def handwritingMoment():
    return 0


def createFeatures(window, indStart, windowSize, data):

    #dummy feature


    #print(data)

    #avgAccX = sum(data['accX'])/len(data['accX'])
    # print(avgAccX)

    return 0