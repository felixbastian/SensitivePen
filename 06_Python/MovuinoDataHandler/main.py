import dataSet.SensitivePenDataSet as sp
import dataSet.GlobalDataSet as gds
import dataSet.MovuinoDataSet as dm
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

toExtract = True
toDataManage = True
toVisualize = True

filter = 25


sep = ","
decimal = "."
##### If no extract
file_start = 1
nbRecord = 10
end = 10

###################################

nb_files = 0

path = folderPath + fileName


# --------- Data Extraction from Movuino ----------
if toExtract:
    movExt.MovuinoExtraction(serialPort, path)


if toDataManage:
    for i in range(file_start, file_start+nbRecord+1):
        dataSet = sp.SensitivePenDataSet(folderPath + fileName + "_" + str(i), filter)
        dataSet.DataManage()
        Te = dataSet.Te
        print("sample frequency : "+str(1/Te))

        if toVisualize:
            dataSet.VisualizeData()

if toVisualize:
    for i in range(file_start, file_start+nbRecord+1):
        sp.SensitivePenDataSet.PlotCompleteFile(folderPath + fileName + "_" + str(i) + "_treated_" + device, sep, decimal)



