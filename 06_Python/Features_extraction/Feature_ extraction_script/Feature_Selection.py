import pandas as pd
import numpy as np

from sklearn import linear_model
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import mutual_info_regression
from boruta import BorutaPy
from sklearn.ensemble import RandomForestRegressor


'''
Methods available:
1. Removing Constants (or almost constants)
2. Correlation
3. Lasso
4. Mutual information
5. Tree based method (BORUTA)

How to use:
(Add/remove entries from steps to modify pipeline)


steps = {'Constant_Features': {'frac_constant_values': 0.9},
         'Correlated_Features': {'correlation_threshold': 0.9},
         'Lasso_Remover': {'alpha': 1, 'coef_threshold':1e-05},
         'Mutual_Info_Remover': {'mi_threshold': 0.05},
         'Boruta_Remover': {'max_depth': 10}}  #Random forest features

FS = FeatureSelector()
FS.fit(x, y['BHK_speed'], steps)
FS.transform(x)

'''



#####################################################################################
#########    Helper Classes (where feature selection actually happens    ############
#####################################################################################

class Constant_feature_remover():
    """
    Identifies features that have a large fraction of constant values.
    
    Parameters
    ----------
    X : pandas dataframe
        A data set where each row is an observation and each column a feature.
        
    frac_constant_values: float, optional (default = 0.90)
        The threshold used to identify features with a large fraction of 
        constant values.
        
    Returns
    -------    
    labels: list
        A list with the labels identifying the features that contain a 
        large fraction of constant values.
    """
    
    def __init__(self):
        pass
        
    def get_cols_to_remove(self, X, frac_constant_values = 0.90):
        # Get number of rows in X
        num_rows = X.shape[0]

        # Get column labels
        allLabels = X.columns.tolist()

        # Make a dict to store the fraction describing the value that occurs the most
        constant_per_feature = {label: X[label].value_counts().iloc[0]/num_rows for label in allLabels}

        # Determine the features that contain a fraction of missing values greater than
        # the specified threshold
        labels = [label for label in allLabels if constant_per_feature [label] > frac_constant_values]

        return labels



class Correlated_feature_remover():
    """
    Identifies features that are highly correlated. Let's assume that if
    two features or more are highly correlated, we can randomly select
    one of them and discard the rest without losing much information.
    
    
    Parameters
    ----------
    X : pandas dataframe
        A data set where each row is an observation and each column a feature.
        
    correlation_threshold: float, optional (default = 0.90)
        The threshold used to identify highly correlated features.
        
    Returns
    -------
    labels: list
        A list with the labels identifying the features that contain a 
        large fraction of constant values.
    """
    
    def __init__(self):
        pass
    
    def get_cols_to_remove(self, X, correlation_threshold = 0.90):
    
        # Make correlation matrix
        corr_matrix = X.corr(method = "spearman").abs()


        # Select upper triangle of matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k = 1).astype(np.bool))

        # Find index of feature columns with correlation greater than correlation_threshold
        labels = [column for column in upper.columns if any(upper[column] >  correlation_threshold)]

        return labels



class Lasso_feature_remover():
    
    def __init__(self):
        pass
    
    def get_cols_to_remove(self, x, y, alpha=1, threshold=1e-05):
        
        lasso = linear_model.Lasso(alpha=alpha)
        selector = SelectFromModel(estimator = lasso, threshold=threshold)
        selector.fit(x.fillna(0), y)
        
        removed_features = selector.get_support()
        removed_features_idx = np.where(removed_features==False)[0]
        removed_features = list(x.columns[removed_features_idx])
        
        return removed_features



class Mutual_information_remover():
    
    def __init__(self):
        pass
    
    def get_cols_to_remove(self, x, y, mi_threshold=0.05):
        mutual_info = mutual_info_regression(x.fillna(0), y)
        mi_df = pd.DataFrame(zip(x.columns, mutual_info), columns=['variable', 'mutual_info'])
        labels = list(mi_df[mi_df['mutual_info'] < mi_threshold]['variable'])
        return labels
    


class Boruta_feature_remover():
    
    def __init__(self):
        pass
    
    def get_cols_to_remove(self, x, y, kwargs={}):
        rf = RandomForestRegressor(**kwargs)
        boruta = BorutaPy(rf, alpha=0.01, n_estimators='auto', verbose=0)
        boruta.fit(x.fillna(0).values, y)
        
        removed_features = boruta.support_
        removed_features_idx = np.where(removed_features==False)[0]
        removed_features = list(x.columns[removed_features_idx])
        
        return removed_features


#####################################################################################
##############       Main class (puts together the pipeline)        #################
#####################################################################################



class FeatureSelector():
    def __init__(self):
        self.features_to_delete = []
        self.available_methods = ['Constant_Features', 'Correlated_Features', 'Lasso_Remover',
                                  'Mutual_Info_Remover', 'Boruta_Remover']
        
        # Define methods
        self.ConstFeatureRemover = Constant_feature_remover()
        self.CorrFeatureRemover = Correlated_feature_remover()
        self.LassoFeatureRemover = Lasso_feature_remover()
        self.MutualInfoRemover = Mutual_information_remover()
        self.BorutaFeatureRemover = Boruta_feature_remover()
        
    def fit(self, x, y, steps = {}):
        
        # Do not make changes to original df (for now) + keep only numeric variables
        x_temp = x.select_dtypes(['number']).copy()
        # x_temp = x.copy()
        
        # Check validity of call
        for key in steps.keys():
            if key not in self.available_methods: raise ValueError(f'Method {key} not defined')
        
        
        # Sequentially apply all methods
        for method in steps.keys():
            
            if method == 'Constant_Features':
                features_to_drop = self.ConstFeatureRemover.get_cols_to_remove(x_temp, **steps['Constant_Features'])
                self.features_to_delete.extend(features_to_drop)
                x_temp.drop(columns=features_to_drop, inplace=True)
                
            
            if method == 'Correlated_Features':
                features_to_drop = self.CorrFeatureRemover.get_cols_to_remove(x_temp, **steps['Correlated_Features'])
                self.features_to_delete.extend(features_to_drop)
                x_temp.drop(columns=features_to_drop, inplace=True)
                
            if method == 'Lasso_Remover':
                alpha = steps['Lasso_Remover']['alpha']
                coef_threshold = steps['Lasso_Remover']['coef_threshold']
                
                features_to_drop = self.LassoFeatureRemover.get_cols_to_remove(x_temp, y, alpha, coef_threshold)
                self.features_to_delete.extend(features_to_drop)
                x_temp.drop(columns=features_to_drop, inplace=True)
                
            if method == 'Mutual_Info_Remover':
                features_to_drop = self.MutualInfoRemover.get_cols_to_remove(x_temp, y, **steps['Mutual_Info_Remover'])
                self.features_to_delete.extend(features_to_drop)
                x_temp.drop(columns=features_to_drop, inplace=True)            

            if method == 'Boruta_Remover':
                features_to_drop = self.BorutaFeatureRemover.get_cols_to_remove(x_temp, y, steps['Boruta_Remover'])
                self.features_to_delete.extend(features_to_drop)
                x_temp.drop(columns=features_to_drop, inplace=True) 
                
            # print(method)
            # print(f'Number of features removed: {len(features_to_drop)}')
            # print(f'Features removed: {features_to_drop}')
            # print('-'*100)
            
            
    def transform(self, X):
        
        if self.features_to_delete == None:
            raise ValueError('You first need to use the fit() method to determine the removed features')

        else:
            # Get selected features
            X = X.drop(columns=self.features_to_delete, inplace=True)
        