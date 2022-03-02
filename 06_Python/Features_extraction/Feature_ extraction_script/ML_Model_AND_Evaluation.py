import pandas as pd
import numpy as np
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge

import warnings

warnings.filterwarnings("ignore")

# meta_data_source = "adult_pre_procdessed_meta_data.csv"
# feature_exctracted_source = "ml_test_data.csv"


def remove_cols(df, c):
    for col in c:
        df = df.loc[:, df.columns != col]
    return df


def split_df_in_xy(df, y_choosen):
    x = remove_cols(df, ["BHK_quality", "BHK_speed", "subjectLabel"])
    y = df[y_choosen]
    return x, y  # train_test_split(x, y)


def get_Random_Forest_Regressor_feature_importance(rf, x, y):
    features = x.columns
    importances = rf.feature_importances_
    for name, importance in zip(features, importances):
        print(name, "=", importance)

    indices = np.argsort(importances)
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()
    return [features[i] for i in indices]


def rmse(score):
    rmse = np.sqrt(-score)
    print("RMSE", rmse)

def pipeline(df):
    #df_extracted_features = pd.read_csv(feature_exctracted_source).iloc[:, 1:]  # ignore old index
    #df_meta_data = pd.read_csv(meta_data_source).iloc[:, 1:]
    #print("columns df_extracted_features", df_extracted_features.columns)
    #print("columns meta data", df_meta_data.columns)
    #df_combined = pd.merge(df_extracted_features, df_meta_data, how="inner", on="subject")

    #  some transformation should happen --> maybe only after splitting data in test and train as suggested by
    #  Devillaine2021

    # split in training and test data
    x, y = split_df_in_xy(df=df, y_choosen="BHK_quality")  # for y we need to check again how to handle speed score

    # apply Random Forest Regressor and get importance
    rnd_clf = RandomForestRegressor(random_state=42)  # create the rf regressor
    rnd_clf.fit(x, y)  # fit it to the data

    # get importance
    fr_desc_importance = get_Random_Forest_Regressor_feature_importance(rnd_clf, x, y)

    x_slected = x[fr_desc_importance[:5]]  ### select a numebr of features

    ## include k-fold, include validation set split
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    print("Random Forrest Regression")
    score = cross_val_score(RandomForestRegressor(random_state=42), x, y, cv=kf, scoring="neg_mean_squared_error")
    rmse(score.mean())



    print("Ridge Regression")
    score = cross_val_score(Ridge(), x, y, cv=kf, scoring="neg_mean_squared_error")
    rmse(score.mean())