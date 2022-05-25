import pandas as pd
import numpy as np
from scipy.signal import welch 

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

def altitude_percentile(df, percentile=0.6):
    features = {}
    
    #will output eg. 'AL_percentile_60' for percentile=0.6
    features['AL_percentile_' + str(int(percentile*100))] = [df['theta'].quantile(percentile)]

    return features


def calculate_median_of_Power_Spectral_of_speed_of_tilt_y_change(df):
    '''
    Input: window
    Output: median_of_Power_Spectral_of_speed_of_tilt_y_change
    '''
    features = {}
    altitude_change_speed = df["theta"].diff().diff()
    _, psd = welch(altitude_change_speed.values[2:])
    features["median_of_Power_Spectral_of_speed_of_tilt_y_change"] = [np.median(psd)]
    return features


def calculate_bandwidth_of_power_spectral_of_speed_of_tilt_x_change(df):
    '''
    Input: window
    Output: bandwidth_of_power_spectral_of_speed_of_tilt_x_change
    '''
    features = {}
    azimuth_change_speed = df["psi"].diff().diff()
    _, psd = welch(azimuth_change_speed.values[2:])
    features["bandwidth_of_power_spectral_of_speed_of_tilt_x_change"] = [np.max(psd)-np.min(psd)]
    return features




def tiltFeatures(df):

    #create features
    features_AZ = tilt_azimuth(df)

    features_AL = tilt_altitude(df)
    features_AZ_diff = tilt_azimuth_change(df)
    features_AL_diff = tilt_altitude_change(df)

    features_AL_percentile = altitude_percentile(df)
    features_median_of_Power_Spectral_of_speed_of_tilt_y_change = calculate_median_of_Power_Spectral_of_speed_of_tilt_y_change(df)
    features_bandwidth_of_power_spectral_of_speed_of_tilt_x_change =calculate_bandwidth_of_power_spectral_of_speed_of_tilt_x_change(df)

    #add features to DataFrame
    all = [features_AZ,features_AL,features_AZ_diff,features_AL_diff,features_median_of_Power_Spectral_of_speed_of_tilt_y_change,
           features_bandwidth_of_power_spectral_of_speed_of_tilt_x_change]
    tilt_df = pd.concat([pd.DataFrame.from_dict(i) for i in all], axis =1)

    return tilt_df
