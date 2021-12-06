import dataSet.SensitivePenDataSet as sp

############ SETTINGS #############

device = 'sensitivePen'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\..\\08_DataPen\\testESP32\\"
fileName = "record"


start = 1
end = 5

sep = ","
decimal = "."
###################################

if __name__ == "__main__":
    for i in range(start, end+1):
        if (device == 'sensitivePen'):
            sp.SensitivePenDataSet.PlotCompleteFile(folderPath + fileName + "_" + str(i) + "_treated_" + device, sep, decimal)
        else:
            print("No device matching")