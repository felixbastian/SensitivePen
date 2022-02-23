import pandas as pd
import numpy as np

#calculating mean, max, min SD of tilt-azimuth
def tilt_azimuth(df):
    print('test')
    mean = 0
    max = 0
    min = 0
    SD = 0

    return mean, max, min, SD

def kinematicFeatures(df):

    #create tilt_azimuth features
    mean_AZ, max_AZ, min_AZ, SD_AZ = tilt_azimuth(df)

    #add features to DataFrame
    kinematicDataFrame = pd.DataFrame([mean_AZ, max_AZ, min_AZ, SD_AZ])


    return kinematicDataFrame