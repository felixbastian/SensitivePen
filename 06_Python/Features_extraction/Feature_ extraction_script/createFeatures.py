import numpy as np

def createFeatures(data):

    #dummy feature
    print(data)
    avgAccX = sum(data['accX'])/len(data['accX'])
    # print(avgAccX)

    return 0