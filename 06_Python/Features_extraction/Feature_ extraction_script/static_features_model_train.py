import getFeaturesFromFile
import getFeaturesWindows
import plot
import pandas as pd
import MathUtilities
import calculateTip
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import integrate
from statsmodels.tsa.statespace.tools import diff
import ML_Model_AND_Evaluation
import static_features_NN_train

# Put the path of the directory where the data is located (keep the r before the string)
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\06_Python\Features_extraction\Data\goodata\Openclose'
# path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands'
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\testing_files\test1\test_1_tilt_on_paper.csv'
# subjectLabels = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Data_summary.xlsx',header=0)
# jen path
path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands'
subjectLabels = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Data_summary_children.xlsx',header=0)
staticScore = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Children\BHK_static_scoring_children.xlsx',header=0)




def runfeaturesextract():
    total_df = []

    # Go through the file indexing all existing files
    for ind in subjectLabels.index:
        # print(subjectLabels[scope][ind])
        # print(staticScore.loc[staticScore['ID'] == subjectLabels['Subject'][ind]])
        staticScoring = staticScore.loc[staticScore['ID'] == subjectLabels['Subject'][ind]]
    #for ind in range(1):

        #some probands do not have data -> skip
        try:
            # DataFrame Creation with the Data by looking up the link in the excel file corresponding to proband
            reference = '/' + subjectLabels['Dataset'][ind] + '/' + subjectLabels[scope][ind] + '.csv'
            link = path + reference
            #link = path
            raw_df = pd.read_csv(link)
            df = raw_df[['time', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'psi', 'theta', 'normAccel', 'normMag','normGyr']]

            #padding (taking away at beginning and end
            # df=df.iloc[padding:(len(df)-padding),:]

            # df = pd.DataFrame()
            # df = df.append(pd.DataFrame(getFeaturesFromFile.datafromfile(path + '\\' + filename)), ignore_index=True)
            # #df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']

            #When the length of the df changes, also change "getFeaturesFromFile.py"
            df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ','psi','theta','normAccel','normMag','normGyr']

            #topDF
            totalDF = df[["time", "accX", 'accY', 'accZ','normAccel','psi','theta']]

            totalDF = totalDF.rename(columns={'accX': "accX_Top", 'accY': "accY_Top", 'accZ': "accZ_Top"})

            total_df.append([staticScoring['ID'], totalDF, staticScoring['critere_1']])
            #calculate integration

            # integrate.cumtrapz(totalDF['accX_Top'],initial = 0)
            accX_top_diff = diff(totalDF['accX_Top'], k_diff=1)
            accY_top_diff = diff(totalDF['accY_Top'], k_diff=1)
            accZ_top_diff = diff(totalDF['accZ_Top'], k_diff=1)
            acc_comb = round(accX_top_diff + accY_top_diff + accZ_top_diff,5)




            #total_df = pd.concat([total_df,featuresByWindowDF], axis=0)
        except TypeError:
            pass
    total_df = pd.DataFrame(total_df)
    return total_df


if __name__ == "__main__":

    # define windowsize
    windowSize = 500

    #define padding (amount to take away at beginning and end of each dataset)
    #not functional yet.. leads to errors
    # padding = 200

    #define the overlapping ratio meaning: windowStart += math.floor(dataWindow / overlapRatio)
    # 1 is resulting in no overlap
    # 2 results in 50% overlap
    overlapRatio = 1

    #define scope: 'Link_loops'/'Link_sentences'
    scope = 'Link_sentences'

    #extract features by window
    total_df = runfeaturesextract()

    #export
    #total_df.to_excel("Data_summary.xlsx")

    #run training model
    #total_df.to_excel("NN_train_data.xlsx")
    static_features_NN_train.pipeline(total_df)
    #run model pipeline and predict
    #ML_Model_AND_Evaluation.pipeline(total_df)


