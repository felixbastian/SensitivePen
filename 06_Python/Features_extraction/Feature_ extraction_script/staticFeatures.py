import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.tools import diff

#calculating mean, max, min SD of tilt-azimuth
def differentiate(df):
    mean = 0
    max = 0
    min = 0
    SD = 0

    return mean, max, min, SD

def staticFeatures(df):

    #differentiate
    mean_AZ, max_AZ, min_AZ, SD_AZ = differentiate(df)

    #add features to DataFrame
    staticDataFrame = pd.DataFrame([mean_AZ, max_AZ, min_AZ, SD_AZ])


    return staticDataFrame