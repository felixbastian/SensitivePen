import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.tools import diff

#calculating mean, max, min SD of tilt-azimuth
def differentiate(df):

    mean = 0
    max = 0
    min = 0
    SD = 0

    features = {}
    features["static_mean"] = [mean]
    features["static_max"] = [max]
    features["static_min"] = [min]
    features["static_SD"] = [SD]


    return features

def staticFeatures(df):

    #differentiate
    features_diff = differentiate(df)

    #add features to DataFrame
    all = [features_diff]
    static_df = pd.concat([pd.DataFrame.from_dict(i) for i in all], axis =1)


    return static_df