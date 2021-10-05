import dataSet.SensitivePenDataSet as sp
import tools.GetAngleMethods as gam
import tools.stockData as sd
import tools.movuinoExtraction as movExt
import tools.FilterMethods as fm
import tools.dataDisplaying.DisplayPenData as dpd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox
from matplotlib.ticker import MultipleLocator

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\data_usefull\\test\\"
fileName = "record"  # generic name numbers will be added for duplicates

serialPort = 'COM4'

toExtract = False
toDataManage = True
toVisualize = False

filter = 25

sep = ","
decimal = "."

###################################

# --------- Data Extraction from Movuino ----------
if toExtract:
    movExt.MovuinoExtraction(serialPort, folderPath + fileName)


# -------- Data processing ----------------------

file_start = 1
end = 2

if toDataManage:
    for i in range(file_start, end+1):
        dataSet = sp.SensitivePenDataSet(folderPath + fileName + "_" + str(i))
        Te = dataSet.Te
        print("sample frequency : "+str(1/Te))
        print(len(dataSet.acceleration))

        #Filtering
        dataSet.acceleration_lp = fm.MeanFilter(dataSet.acceleration, 10)
        dataSet.gyroscope_lp = fm.MeanFilter(dataSet.gyroscope, 10)
        dataSet.magnetometer_lp = fm.MeanFilter(dataSet.magnetometer, 10)

        #ComputeAngles
        dataSet.sensitivePenAngles = gam.computePenAngles(dataSet)

        #Features
        # Difference between runcode et runfeatures extract

        #stock in processed.csv
        sd.stockProcessedData(dataSet, dataSet.filepath + "_treated_" + dataSet.name + ".csv")

        #display
        dpd.DispProcessedData(sensitivPen=dataSet)
        dpd.DispRawData(sensitivPen=dataSet)
        dpd.DispOnlyPenAngles(sensitivPen=dataSet)


if toVisualize:
    """
    """




