import getFeaturesFromFile
import getFeaturesWindows
import plot
import pandas as pd
import MathUtilities
import os
import numpy as np
# Put the path of the directory where the data is located (keep the r before the string)
path = r'C:\Users\CRI User\Documents\GitHub\PythonDFTMotionP3\goodata\Openclose'

def runfeaturesextract():

    # Go thru the folder with all datas
    for filename in os.listdir(path):

        # DataFrame Creation with the Data
        df = pd.DataFrame()
        df = df.append(pd.DataFrame(getFeaturesFromFile.datafromfile(path+'\\'+filename)), ignore_index=True)
        df.columns = ['time', 'accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ']

    # Datatype is the axis of data you want, you just have to replace by the correpsonding column. (exemple 'accX')
    datatype = ['accZ']

    # Operations for Different versions of Data
    Data = df[datatype]
    df['norme'] = MathUtilities.norme(df)
    norme = df['norme']

    # Get Features by Window
    # Choose Data or Norme :)
    Xfinaldata, Yfinaldata = getFeaturesWindows.getFeaturesWindows(norme, 1)

    # Create final DataFrame
    dffinaldata = pd.DataFrame(Xfinaldata)
    dffinaldata.columns = ['DC', 'energy', 'entropyDFT', 'Deviation']

    # This show the final dataframe in the interpreter
    print(dffinaldata)

    # This plot the little dashboard with the distributions of values
    plot.plotfeaturesnotarget(dffinaldata)

        # This command create the new file with extracted features.
        # You could replace the path with where you want the file to be stocked in.
        # after the last \ you just have to write the name you want for the file and finish by .csv.
        # Then, you can click on the Play Button :)
    #dffinaldata.to_csv(r'C:\Users\CRI User\Desktop\DataSets\openclosepierro.csv')

runfeaturesextract()

