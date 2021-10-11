import dataSet.SensitivePenDataSet as sp
import dataSet.GlobalDataSet as gds

############ SETTINGS #############

device = 'SensitivePen'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "/Users/phelippeau/Documents/PhD/Data/Test_Postures/Cross_Thumb/"
fileName = "record"

start = 1
end = 6

sep = ","
decimal = "."
###################################

if __name__ == "__main__":
    for i in range(start, end+1):
        if (device == 'SensitivePen'):
            sp.SensitivePenDataSet.PlotCompleteFile(folderPath + fileName + "_" + str(i) + "_treated_" + device, sep, decimal)
        elif (device == 'globalDataSet'):
            dataSet = gds.GlobalDataSet.PlotCompleteFile(folderPath + fileName, sep, decimal)
        else:
            print("No device matching")