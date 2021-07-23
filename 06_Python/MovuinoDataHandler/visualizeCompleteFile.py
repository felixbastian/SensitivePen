import dataSet.SensitivePenDataSet as sp
import dataSet.SkateboardXXX3000DataSet as sk
import dataSet.GlobalDataSet as gds

############ SETTINGS #############

device = 'SensitivePen'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\_data\\test_ecriture_live\\"
fileName = "record"

start = 1
end = 5

sep = "\t"
decimal = ","
###################################

if __name__ == "__main__":
    for i in range(start, end+1):
        if (device == 'SensitivePen'):
            sp.SensitivePenDataSet.PlotCompleteFile(folderPath + fileName + "_" + str(i) + "_treated_" + device, sep, decimal)
        elif (device == 'skateboardXXX3000'):
            sk.SkateboardXXX3000DataSet.PlotCompleteFile(folderPath + fileName, sep, decimal)
        elif (device == 'globalDataSet'):
            dataSet = gds.GlobalDataSet.PlotCompleteFile(folderPath + fileName, sep, decimal)
        else:
            print("No device matching")