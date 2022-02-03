import glob
import os
import numpy as np
import getFeaturesWindows
dataWindow = 20
def datafromfile(file):

    # Open File
        curFile = open(file,"r")
        dataFile = curFile.read().split("\n")
        rowData = np.empty((1, 16))  # [time, accX, accY, accZ, gyrX, gyrY, gyrX, magY, magY, magZ]
        rowData[:] = np.NaN
        if len(dataFile)>= dataWindow:
            for j in range(1,len(dataFile)):
                data = dataFile[j].split(",")
                if (len(data)==16):

                    # Get Data
                    rowData = np.append(rowData, [[float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]),float(data[6]),float(data[7]),float(data[8]),float(data[9]),float(data[10]), float(data[11]),float(data[12]),float(data[13]),float(data[14]),float(data[15])]], axis=0)
            rowData = rowData[1:, :]
            return(rowData)
            curFile.close()
