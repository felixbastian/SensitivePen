import dataSet.SensitivePenDataSet as sp
import dataSet.GlobalDataSet as gds
import dataSet.MovuinoDataSet as md
import tools.DisplayFunctions as df
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import tools.movuinoExtraction as movExt

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


file_start = 1
end = 2

# -------- Data processing ----------------------
if toDataManage:
    for i in range(file_start, end+1):
        dataSet = md.MovuinoDataSet(folderPath + fileName + "_" + str(i))
        Te = dataSet.Te
        print("sample frequency : "+str(1/Te))
        print(len(dataSet.acceleration))

        #Filtering
        #ComputeAngles
        #Features
        #stock in processed.csv

if toVisualize:
    """
    for i in range(file_start, end+1):
        a=0
        #sp.SensitivePenDataSet.PlotCompleteFile(folderPath + fileName + "_" + str(i) + "_treated_" + device, sep, decimal)
        #Plot angles
        #plot raw && filtered processed data
        #plot features
    """



