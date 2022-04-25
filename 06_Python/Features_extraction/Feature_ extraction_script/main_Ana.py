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

# Put the path of the directory where the data is located (keep the r before the string)
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\06_Python\Features_extraction\Data\goodata\Openclose'
# path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands'
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\testing_files\test1\test_1_tilt_on_paper.csv'
# subjectLabels = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Data_summary.xlsx',header=0)
# jen path
# path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands'
# subjectLabels = pd.read_excel(r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\09_Data_probands\Data_summary_children.xlsx',header=0)

path = r'../../../09_Data_probands'



# 09_Data_probands/Data_summary_children.xlsx

def runfeaturesextract(subjectLabels):
    total_df = pd.DataFrame()

    #filter the database to only include the desired scope

    subjectLabels = subjectLabels[subjectLabels['Dataset']==datasetScope]
    # Go through the file indexing all existing files
    for ind in subjectLabels.index:
        print(subjectLabels[scope][ind])
    #for ind in range(1):

        #some probands do not have data -> skip
        try:
            # DataFrame Creation with the Data by looking up the link in the excel file corresponding to proband
            reference = '/' + subjectLabels['Dataset'][ind] + '/' + subjectLabels[scope][ind] + '.csv'
            link = path + reference
            #link = path
            start, end = subjectLabels['Start'][ind], subjectLabels['End'][ind]


            raw_df = pd.read_csv(link)
            #raw_df = raw_df.iloc[start:end,:]

            raw_df = raw_df.loc[start:end,:]
            raw_df = raw_df.reset_index()
            #print(raw_df)
            df = raw_df[['time', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'psi', 'theta', 'normAccel', 'normMag','normGyr']]
            #df = df.iloc[start:end,:]

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

            #totalDF = df[["time", "accX", 'accY', 'accZ']].rename(index={1: "AccX_Top", 2: "AccY_Top", 3: "AccZ_Top"})
            #tipDF is the dataframe that contains the vectors of the tip of the pen (Acceleration in three directions + psi, theta)
            tipDF = calculateTip.calculateTip(totalDF)
            totalDF = pd.concat([totalDF,tipDF], axis=1)

            #calculate integration

            # integrate.cumtrapz(totalDF['accX_Top'],initial = 0)
            accX_top_diff = diff(totalDF['accX_Top'], k_diff=1)
            accY_top_diff = diff(totalDF['accY_Top'], k_diff=1)
            accZ_top_diff = diff(totalDF['accZ_Top'], k_diff=1)
            acc_comb = round(accX_top_diff + accY_top_diff + accZ_top_diff,5)

            # plt.figure()
            # sns.lineplot(totalDF['time'], totalDF['accY_Tip'])
            # sns.lineplot(totalDF['time'], totalDF['accY_Top'])
            # plt.show()
            #sns.lineplot(totalDF['time'], totalDF['accY_Tip'])
            #sns.lineplot(totalDF['time'], totalDF['accZ_Top'])
            #plt.show()

            #sns.lineplot(totalDF['time'], totalDF['psi'])
            #sns.lineplot(totalDF['time'], totalDF['theta'])
            # plt.show()

            # sns.lineplot(data['time'], data['accY_Top'])
            # sns.lineplot(data['time'], data['accZ_Top'])


            ##DATA EXPORT FOR ANA
            # padding = 200
            # totalDF=totalDF.iloc[padding:(len(totalDF)-padding),:]
            # windowSize = len(totalDF)

            # Pass dataframe through window and set isRaw to False
            featuresByWindowDF = getFeaturesWindows.passThroughWindow(totalDF, False, windowSize, overlapRatio)

            # Insert label of subject
            featuresByWindowDF.insert(0, 'subjectLabel', subjectLabels['Dataset'][ind] + "_" + subjectLabels['Subject'][ind])

            #Insert BHK scores of subject
            featuresByWindowDF.insert(1, 'BHK_speed', subjectLabels['Speed_score'][ind])
            featuresByWindowDF.insert(2, 'BHK_quality', subjectLabels['Quality_score'][ind])

            #Add Age and Gender to the features
            featuresByWindowDF["Age"] = subjectLabels["Age"][ind]
            featuresByWindowDF["Gender"] = int(subjectLabels["Gender (0=boys)"][ind])

            pd.set_option('display.max_columns', None)
            #print(featuresByWindowDF.head())

            # print('Final dataframe for model')
            # print(len(featuresByWindowDF))
            #print(featuresByWindowDF.head())
            total_df = pd.concat([total_df,featuresByWindowDF], axis=0)
        except TypeError:
            pass
    return total_df


if __name__ == "__main__":

    path = r"../../../09_Data_probands/"
    subjectLabels = pd.read_excel(path + 'Data_summary_children.xlsx', header=0)

    # define windowsize
    windowSize = 300

    #define padding (amount to take away at beginning and end of each dataset)
    #not functional yet.. leads to errors
    # padding = 200

    #define the overlapping ratio meaning: windowStart += math.floor(dataWindow / overlapRatio)
    # 1 is resulting in no overlap
    # 2 results in 50% overlap
    overlapRatio = 1

    #define scope: 'Link_loops'/'Link_sentences'
    scope = 'Link_sentences'

    #define scope of Dataset
    datasetScope = 'Children'

    #extract features by window
    total_df = runfeaturesextract(subjectLabels)




    #we take the features out for model creation
    total_df = total_df.drop(columns=['Age', 'Gender'])

    #export
    total_df.to_excel("Data_summary.xlsx")

    #new_df = total_df.apply(lambda x: total_df['subjectLabel'].values)

    #run model pipeline and predict
    ML_Model_AND_Evaluation.pipeline(total_df)


