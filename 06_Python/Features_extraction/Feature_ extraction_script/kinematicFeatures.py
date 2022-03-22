import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.tools import diff
from scipy.stats import skew
from scipy.stats import entropy
from scipy.signal import argrelmax
from scipy.signal import argrelmin

# calculating mean, max, min SD of tilt-azimuth
def acceleration_basic_stats(df):
    print(df.head(3))
    mean = df['normAccel'].mean()
    max = df['normAccel'].max()
    min = df['normAccel'].min()
    SD = df['normAccel'].std()

    features = {}
    features["acceleration_mean"] = [mean]
    features["acceleration_max"] = [max]
    features["acceleration_min"] = [min]
    features["acceleration_D"] = [SD]

    return features

def get_jerk(df):
    features = {}

    # Approximate jerk
    df['jerk'] = df['normAccel'].diff() / df['time'].diff()
    # First row is Nan, second row is very large value because first row of normAccel is 0
    # For simplicity replace both values with mean -> won't skew the results that much
    df['jerk'][:2] = df['jerk'].mean()

    features['jerk_mean'] = [df['jerk'].mean()]
    features['jerk_max'] = [df['jerk'].max()]
    features['jerk_min'] = [df['jerk'].min()]
    features['jerk_std'] = [df['jerk'].std()]

    features['jerk_mad'] = [df['jerk'].mad()]
    features['jerk_skew'] = [skew(df['jerk'])]
    features['jerk_entropy'] = [entropy(df['jerk'].value_counts())]

    return features

def nb_peaks_acceleration(df):
    acc = np.array(df["normAccel"])
    features = {}
    #nb of local max and local min normalized by the length of the time series
    features["nb_max_acc"] = [len([argrelmax(acc)[0]])/len(acc)]
    features["nb_min_acc"] = [len([argrelmin(acc)[0]])/len(acc)]
    return features


def kinematicFeatures(df):
    # differentiate
    features_diff = acceleration_basic_stats(df)
    features_jerk = get_jerk(df)
    features_peaks = nb_peaks_acceleration(df)

    # add features to DataFrame
    all = [features_diff, features_jerk, features_peaks]
    kinematic_df = pd.concat([pd.DataFrame.from_dict(i) for i in all], axis=1)

    return kinematic_df