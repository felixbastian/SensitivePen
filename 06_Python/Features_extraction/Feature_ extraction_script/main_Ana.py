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
path = r'/Users/jedrzejalchimowicz/Documents/GitHub/SensitivePen/09_Data_probands'
subjectLabels = pd.read_excel(r'/Users/jedrzejalchimowicz/Documents/GitHub/SensitivePen/09_Data_probands/Data_summary.xlsx',header=0)

def runfeaturesextract():
    total_df = pd.DataFrame()

    # Go through the file indexing all existing files
    for ind in subjectLabels.index:
    #for ind in range(1):

        # DataFrame Creation with the Data by looking up the link in the excel file corresponding to proband
        reference = '/' + subjectLabels['Dataset'][ind] + '/' + subjectLabels[scope][ind] + '_treated_SensitivePen.csv'
        link = path + reference
        #link = path
        raw_df = pd.read_csv(link)
        df = raw_df[['time', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'psi', 'theta', 'normAccel', 'normMag','normGyr']]


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
        tipDF = calculateTip.calculateTip(df)
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

        #Pass dataframe through window and set isRaw to False

        featuresByWindowDF = getFeaturesWindows.passThroughWindow(totalDF, False, windowSize, overlapRatio)

        # Insert label of subject
        featuresByWindowDF.insert(0, 'subjectLabel', subjectLabels['Dataset'][ind] + "_" + subjectLabels['Subject'][ind])

        #Insert BHK scores of subject
        featuresByWindowDF.insert(1, 'BHK_speed', subjectLabels['Speed_score'][ind])
        featuresByWindowDF.insert(2, 'BHK_quality', subjectLabels['Quality_score'][ind])

        # print('Final dataframe for model')
        # print(len(featuresByWindowDF))
        #
        # print(featuresByWindowDF.head())
        total_df = pd.concat([total_df,featuresByWindowDF], axis=0)

    return total_df


if __name__ == "__main__":

    # define windowsize
    windowSize = 30

    #define the overlapping ratio meaning: windowStart += math.floor(dataWindow / overlapRatio)
    # 1 is resulting in no overlap
    # 2 results in 50% overlap
    overlapRatio = 1

    #define scope: 'Link_loops'/'Link_sentences'
    scope = 'Link_sentences'

    #extract features by window
    total_df = runfeaturesextract()


    #data export
    # total_df.to_csv('total_df_sentences.csv', sep=',')

    #run model pipeline and predict
    ML_Model_AND_Evaluation.pipeline(total_df)


