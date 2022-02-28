import pandas as pd
import numpy as np

#general function that computes all stats
def add_stats(column):
    mean = column.mean()
    max = column.max()
    min = column.min()
    std = column.std()
    var = column.var()
    return mean, max, min, std, var

#calculating mean, max, min SD of tilt-azimuth
def tilt_azimuth(df):
    '''
    Input: window
    Output: mean, max, min, std and var of azimuth in the window
    '''
    azimuth = df["psi"]
    features = {}
    mean, max, min, std, var = add_stats(azimuth)
    features["AZ_mean"] = [mean]
    features["AZ_max"] = [max]
    features["AZ_min"] = [min]
    features["AZ_std"] = [std]
    features["AZ_var"] = [var]

    return features

def tilt_azimuth_change(df):
    '''
    Input: window
    Output: mean, max, min, std and var of azimuthm change in the window
    '''
    azimuth_change = df["psi"].diff()
    features = {}
    mean, max, min, std, var = add_stats(azimuth_change)
    features["AZ_diff_mean"] = [mean]
    features["AZ_diff_max"] = [max]
    features["AZ_diff_min"] = [min]
    features["AZ_diff_std"] = [std]
    features["AZ_diff_var"] = [var]

    return features

def tilt_altitude(df):
    '''
    Input: window
    Output: mean, max, min, std and var of altitude in the window
    '''
    altitude = df["theta"]
    features = {}
    mean, max, min, std, var = add_stats(altitude)
    features["AL_mean"] = [mean]
    features["AL_max"] = [max]
    features["AL_min"] = [min]
    features["AL_std"] = [std]
    features["AL_var"] = [var]

    return features

def tilt_altitude_change(df):
    '''
    Input: window
    Output: mean, max, min, std and var of azimuthm change in the window
    '''
    altitude_change = df["theta"].diff()
    features = {}
    mean, max, min, std, var = add_stats(altitude_change)
    features["AL_diff_mean"] = [mean]
    features["AL_diff_max"] = [max]
    features["AL_diff_min"] = [min]
    features["AL_diff_std"] = [std]
    features["AL_diff_var"] = [var]

    return features


def tiltFeatures(df):

    #create features
    features_AZ = tilt_azimuth(df)

    features_AL = tilt_altitude(df)
    features_AZ_diff = tilt_azimuth_change(df)
    features_AL_diff = tilt_altitude_change(df)

    #add features to DataFrame
    all = [features_AZ,features_AL,features_AZ_diff,features_AL_diff]
    tilt_df = pd.concat([pd.DataFrame.from_dict(i) for i in all], axis =1)

    return tilt_df