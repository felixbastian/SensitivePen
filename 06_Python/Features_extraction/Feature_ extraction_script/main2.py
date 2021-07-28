import getFeaturesFromFile
import getFeaturesWindows
import plot
from sklearn import preprocessing
import pandas as pd
import MathUtilities
import os, fnmatch
datatype = 'accZ'
path = r'C:\Users\CRI User\Documents\GitHub\PythonDFTMotionP3\goodata\atelle'
pattern = "*good*"

def runcode():
    # Set up empty Dataframes
    dfbad = pd.DataFrame()
    dfgood = pd.DataFrame()

    # Go thru the files and extract them depending on the pattern
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, pattern):  # Yellow dots

            # Get Data
            df = pd.DataFrame()
            df = df.append(pd.DataFrame(getFeaturesFromFile.datafromfile(path + '\\' + filename)), ignore_index=True)
            #df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']

            # Normalize
            #x = df
            #min_max_scaler = preprocessing.MinMaxScaler()
            #x_scaled = min_max_scaler.fit_transform(x)
            #df = pd.DataFrame(x_scaled)
            df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']

            # Select and set up Data
            data = df[datatype]
            #alldata = df
            df['integral'] = MathUtilities.integral(df, data)
            integral = df['integral']
            df['derivate'] = MathUtilities.derivData(df, data)
            derivate = df['derivate']
            angle = MathUtilities.angle(df, df.accX, df.accZ)
            norme = MathUtilities.norme(df)

            # Get Features by Window
            Xbad,Ybad = getFeaturesWindows.getFeaturesWindows(norme, 1)

            # Create DataFrame with Bad Examples
            dfxbad = pd.DataFrame(Xbad)
            dfxbad.columns = ['DC', 'energy', 'entropyDFT', 'Deviation']
            dfybad = pd.DataFrame(Ybad)
            dfybad.columns = ['target']
            dfbad = dfbad.append(pd.concat([dfxbad,dfybad],axis=1))

        else: # Purple dots

            # Get Data
            df = pd.DataFrame()
            df = df.append(pd.DataFrame(getFeaturesFromFile.datafromfile(path + '\\' + filename)), ignore_index=True)
            df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']

            # Select and set up Data
            data = df[datatype]
            df['integral'] = MathUtilities.integral(df, data)
            integral = df['integral']
            df['derivate'] = MathUtilities.derivData(df, data)
            derivate = df['derivate']
            angle = MathUtilities.angle(df, df.accX, df.accZ)
            norme = MathUtilities.norme(df)

            # Get Features by Window
            Xgood, Ygood = getFeaturesWindows.getFeaturesWindows(norme, 0)

            # Create DataFrame with Bad Examples
            dfxgood = pd.DataFrame(Xgood)
            dfxgood.columns = ['DC', 'energy', 'entropyDFT', 'Deviation']
            dfygood = pd.DataFrame(Ygood)
            dfygood.columns = ['target']
            dfgood = dfgood.append(pd.concat([dfxgood, dfygood], axis=1))

    # Create Final DataFrame
    dfinal = pd.concat([dfgood, dfbad], axis=0)
    #Normalize
    h = dfinal
    min_max_scaler = preprocessing.MinMaxScaler()
    h_scaled = min_max_scaler.fit_transform(h)
    dfinal = pd.DataFrame(h_scaled)
    dfinal.columns = ['DC', 'energy', 'entropyDFT', 'Deviation', 'target']
    #dfi.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']
    print (dfinal)
    #print(dfinal)
    #plot.plotfeatures(dfinal)
    plot.plotfeatures(dfinal)

    #plotlyplot.plotdatabeautyful(dfinal)
    plot.plotdata(df, integral, derivate, angle)
    #dfinal.to_csv(r'C:\Users\CRI User\Desktop\DataSets\atelle_ananorme.csv')

runcode()
