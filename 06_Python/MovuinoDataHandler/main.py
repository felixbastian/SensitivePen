import serial
import dataSet.SensitivePenDataSet as sp
import dataSet.GlobalDataSet as gds
import dataSet.MovuinoDataSet as dm
import tools.DisplayFunctions as df
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



############   SETTINGS   #############

device = 'sensitivePen'  # devices available : sensitivePen / globalDataSet

folderPath = "/Users/phelippeau/Documents/PhD/Data/Manips_Garches/"

fileName = "record"  # generic name numbers will be added for duplicates

serialPort = '/dev/cu.usbserial-0154D8DD'

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

    isReading = False
    ExtractionCompleted = False
    arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
    line_byte = ''
    line_str = ''
    datafile = ''
    nbRecord = 1

    # Send read SPIFF instruction to Movuino
    arduino.write(bytes("r", 'ascii'))

    while ExtractionCompleted != True:
        line_byte = arduino.readline()
        line_str = line_byte.decode("utf-8")

        if "XXX_end" in line_str and isReading == True :
            isReading = False
            ExtractionCompleted = True
            print("End of data sheet")

            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.write(datafile)

        if "XXX_newRecord" in line_str and isReading == True :
            print("Add new file")
            with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                file.write(datafile)

            datafile = ''
            line_str = ''
            nbRecord += 1

        if (isReading):
            if line_str != '':
                datafile += line_str.strip() + '\n'

        if ("XXX_beginning" in line_str):
            isReading = True
            print("Record begins")


if toDataManage:
    print(nbRecord)
    #nbRecord = 1
    for i in range(file_start, file_start+nbRecord+1):
        if (device == 'sensitivePen'):
            print("--- Processing : " + folderPath + fileName + "_" + str(i) + " --- ")
            dataSet = sp.SensitivePenDataSet(folderPath + fileName + "_" + str(i), filter)
        elif (device == 'globalDataSet'):
            print("Processing : " + folderPath + fileName + "_" + str(i))
            dataSet = gds.GlobalDataSet(folderPath + fileName + "_" + str(i), filter)
        else:
            print("No device matching")

        dataSet.DataManage()
        Te = dataSet.Te
        print("sample frequency : "+str(1/Te))

        if toVisualize:
            dataSet.VisualizeData()

if toVisualize:
    for i in range(file_start, file_start+nbRecord+1):
        if (device == 'sensitivePen'):
            sp.SensitivePenDataSet.PlotCompleteFile(folderPath + fileName + "_" + str(i) + "_treated_" + device, sep, decimal)
        elif (device == 'globalDataSet'):
            dataSet = gds.GlobalDataSet.PlotCompleteFile(folderPath + fileName, sep, decimal)
        else:
            print("No device matching")


