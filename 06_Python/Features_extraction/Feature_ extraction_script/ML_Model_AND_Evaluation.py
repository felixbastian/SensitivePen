import pandas as pd
import numpy as np
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from Feature_Selection import FeatureSelector
import random
from plotPrediction import plotPrediction
from tqdm import tqdm


import warnings

warnings.filterwarnings("ignore")

# meta_data_source = "adult_pre_procdessed_meta_data.csv"
# feature_exctracted_source = "ml_test_data.csv"


def remove_cols(df, c):
    for col in c:
        df = df.loc[:, df.columns != col]
    return df



def split_df_in_xy(df, y_choosen,index, uniqueChildren):

    split = [uniqueChildren[i] for i in index]
    df = df[df['subjectLabel'].isin(split)]

    label = df['subjectLabel']
    x = remove_cols(df, ["BHK_quality", "BHK_speed", "subjectLabel"])
    y = df[y_choosen]

    return x,y,label


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

def preprocess_nan(x):
    '''
    preprocess Nan in Age and Gender
    substitute Nan with 0 and create a dummy to account for it
    if there are no Nan it does not do anything
    '''
    if x.Age.isna().sum() > 0:
        x["has_age"] = 1
        x.loc[x.Age.isna(), "has_age"] = 0
        x.loc[x.Age.isna(), "Age"] = 0
    if x.Gender.isna().sum() > 0:
        x["has_gender"] = 1
        x.loc[x.Gender.isna(), "has_gender"] = 0
        x.loc[x.Gender.isna(), "Gender"] = 0

def pipeline(df):
    #df_extracted_features = pd.read_csv(feature_exctracted_source).iloc[:, 1:]  # ignore old index
    #df_meta_data = pd.read_csv(meta_data_source).iloc[:, 1:]
    #print("columns df_extracted_features", df_extracted_features.columns)
    #print("columns meta data", df_meta_data.columns)
    #df_combined = pd.merge(df_extracted_features, df_meta_data, how="inner", on="subject")

    #  some transformation should happen --> maybe only after splitting data in test and train as suggested by
    #  Devillaine2021

    ############# Prediction pipeline #################

    predictFrame = pd.DataFrame()

    # we identify the inique children in the database
    uniqueChildren = df['subjectLabel'].unique()
    kf = KFold(n_splits=10, shuffle=True, random_state=3)

    for train_index, test_index in tqdm(kf.split(uniqueChildren)):


        train_x, train_y, train_label = split_df_in_xy(df, 'BHK_quality', train_index, uniqueChildren)
        test_x, test_y, test_label = split_df_in_xy(df, 'BHK_quality',test_index,uniqueChildren)

        # print(train_x)
        # print(train_y)
        # print(train_label)


        #select the features

        ########### Feature Selection ###########
        '''
        steps = {'Constant_Features': {'frac_constant_values': 0.9},
                 'Correlated_Features': {'correlation_threshold': 0.9},
                 'Lasso_Remover': {'alpha': 1, 'coef_threshold': 1e-05},
                 'Mutual_Info_Remover': {'mi_threshold': 0.05},
                 'Boruta_Remover': {'max_depth': 10}
                 }  # Random forest features

        FS = FeatureSelector()
        FS.fit(train_x, train_y, steps)
        FS.transform(train_x)
        '''
        # apply Random Forest Regressor and get importance

        #### Timestmp added at some point!
        train_x = train_x.select_dtypes(['number'])
        #### Remove later

        #train the model

        rnd_clf = RandomForestRegressor(random_state=42)  # create the rf regressor
        rnd_clf.fit(train_x, train_y)  # fit it to the data

        # get importance
        #fr_desc_importance = get_Random_Forest_Regressor_feature_importance(rnd_clf,train_x, train_y)
        #x_slected = train_x[fr_desc_importance[:5]]  ### select a number of features

        #create prediction
        '''
        # FS.transform(test_x)
        '''
        pred = rnd_clf.predict(test_x)
        #save prediction and re-iterate

        #create column iterator
        i=0
        iterCol=[]
        lab = test_label.tolist()
        for x in range(len(lab)):

            if(x==0):
                iterCol.append(0)
                continue
            elif lab[x] == lab[x-1]:
                i= i+1
                iterCol.append(i)
            elif lab[x] != lab[x-1]:
                i = 0
                iterCol.append(0)

        entry = pd.DataFrame([test_label.tolist(), test_y.tolist(), pred.tolist(), iterCol]).T.rename(columns={0:'labels', 1:'y_real', 2:'y_pred',3:'iter'})

        predictFrame = pd.concat([predictFrame,entry], axis=0)



    finalFrame =[]
    for item in predictFrame['labels'].unique():
        data = predictFrame[predictFrame['labels'] == item]
        finalFrame.append([item,data['y_real'].mean(),data['y_pred'].mean()])
    finalFrame = pd.DataFrame(finalFrame).rename(columns={0:'labels', 1:'y_real', 2:'y_pred',3:'iter'})

    plotPrediction(finalFrame)
    # print(predictFrame)
    # print(finalFrame)
    predictFrame.to_csv('selectionOfPrediction.csv')
    finalFrame.to_csv('prediction.csv')


    # predictFrame.apply(lambda x: x)

    #ACTIVATE FOR AGE AND GENDER
    #preprocess_nan(x)
    

# df = pd.read_excel('data_summary.xlsx')
# pipeline(df)

'''

    ## include k-fold, include validation set split
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    print("Random Forest Regression")
    score = cross_val_score(RandomForestRegressor(random_state=42), x, y, cv=kf, scoring="neg_mean_squared_error")
    rmse(score.mean())



    print("Ridge Regression")
    score = cross_val_score(Ridge(), x, y, cv=kf, scoring="neg_mean_squared_error")
    rmse(score.mean())

'''