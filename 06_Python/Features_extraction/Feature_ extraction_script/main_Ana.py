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

# Put the path of the directory where the data is located (keep the r before the string)
#path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\SensitivePen\06_Python\Features_extraction\Data\goodata\Openclose'
path = r'C:\Users\felix\OneDrive\Desktop\DSBA-M2\CRP\testing_files\test1'

def runfeaturesextract():

    # Go thru the folder with all datas
    for filename in os.listdir(path):

        # DataFrame Creation with the Data
        df = pd.DataFrame()
        df = df.append(pd.DataFrame(getFeaturesFromFile.datafromfile(path + '\\' + filename)), ignore_index=True)
        #df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']

        #When the length of the df changes, also change "getFeaturesFromFile.py"
        df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ','psi','theta','normAccel','normMag','normGyr']

    #topDF
    totalDF = df[["time", "accX", 'accY', 'accZ']]
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

    #testing some stuff
    # pd.set_option("display.precision", 8)
    # print(totalDF['accX_Top'].head())
    # print(accX_top_diff[200:210])
    # print(accY_top_diff[200:210])
    # print(accZ_top_diff[200:210])
    # print('result')
    # print(acc_comb[200:210])

    sns.lineplot(totalDF['time'], accX_top_diff)
    #sns.lineplot(totalDF['time'], totalDF['accY_Top'])
    #sns.lineplot(totalDF['time'], totalDF['accZ_Top'])
    plt.show()

    #sns.lineplot(totalDF['time'], totalDF['psi'])
    #sns.lineplot(totalDF['time'], totalDF['theta'])
    plt.show()

    # sns.lineplot(data['time'], data['accY_Top'])
    # sns.lineplot(data['time'], data['accZ_Top'])

    #Pass dataframe through window and set isRaw to False
    #define windowsize
    windowSize = 20
    featuresByWindowDF = getFeaturesWindows.passThroughWindow(totalDF, False, windowSize)
    print(featuresByWindowDF.head())
    
    # Datatype is the axis of data you want, you just have to replace by the correpsonding column. (exemple 'accX')
    datatype = ['accZ']

    # Operations for Different versions of Data
    Data = df[datatype]
    df['norme'] = MathUtilities.norme(df)

    # Get Features by Window

    #Xfinaldata = window of features (based on norm)
    #Yfinaldata = boolean value indicating whether this feature could have been extracted (1) or not (0)
    #window is the 20 units dataframe extraction of "raw" data (time, accX, accY, ...)

    #Xfinaldata, Yfinaldata, window = getFeaturesWindows.passThroughWindow(df, True)

    # Create final DataFrame
    #dffinaldata = pd.DataFrame(Xfinaldata)
    #dffinaldata.columns = ['DC', 'energy', 'entropyDFT', 'Deviation']

    # This show the final dataframe in the interpreter (final meaning the last iteration)

    #final window of raw data
    #print(window)

    #final window of feature extracted data
    #print(dffinaldata)

    # This plot the little dashboard with the distributions of values
    #plot.plotfeaturesnotarget(dffinaldata)

        # This command create the new file with extracted features.
        # You could replace the path with where you want the file to be stocked in.
        # after the last \ you just have to write the name you want for the file and finish by .csv.
        # Then, you can click on the Play Button :)
    #dffinaldata.to_csv(r'C:\Users\CRI User\Desktop\DataSets\openclosepierro.csv')

runfeaturesextract()

