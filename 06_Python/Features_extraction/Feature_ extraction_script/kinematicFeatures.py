import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.tools import diff


# calculating mean, max, min SD of tilt-azimuth
def differentiate(df):
    mean = 0
    max = 0
    min = 0
    SD = 0

    features = {}
    features["kinematic_mean"] = [mean]
    features["kinematic_max"] = [max]
    features["kinematic_min"] = [min]
    features["kinematic_D"] = [SD]

    return features


def kinematicFeatures(df):
    # differentiate
    features_diff = differentiate(df)

    # add features to DataFrame
    all = [features_diff]
    kinematic_df = pd.concat([pd.DataFrame.from_dict(i) for i in all], axis=1)

    return kinematic_df