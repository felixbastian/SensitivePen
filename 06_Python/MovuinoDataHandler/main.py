import dataSet.SensitivePenDataSet as sp
import tools.FilterMethods as fm
import tools.features_extraction_scripts.runFeature as ft
import os

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\Data_Postures\\"
fileName = "record"  # generic name numbers will be added for duplicates
pathfeatures ="zozo.csv"
serialPort = 'COM4'

toExtract = False
toDataManage = True
toVisualize = False

filter = 1

sep = ","
decimal = "."

###################################

# --------- Data Extraction from Movuino ----------
if toExtract:
    """
    Extract data from the serial port and stock it into a csv file
    """
    print("Data extraction..")
    sp.SensitivePenDataSet.MovuinoExtraction(serialPort, folderPath + fileName)


# -------- Data processing ----------------------

file_start = 1
end = 3

if toDataManage:
    for filename in os.listdir(folderPath):
        sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
        Te = sensitivPenDataSet.Te
        print("sample frequency : " + str(1/Te))

        #Filtering
        sensitivPenDataSet.acceleration_lp = fm.MeanFilter(sensitivPenDataSet.acceleration, 10)
        sensitivPenDataSet.gyroscope_lp = fm.MeanFilter(sensitivPenDataSet.gyroscope, 10)
        sensitivPenDataSet.magnetometer_lp = fm.MeanFilter(sensitivPenDataSet.magnetometer, 10)

        #ComputeAngles
        sensitivPenDataSet.computePenAngles()

        #FeaturesDifference between runcode et runfeatures extract
        #ft.getDataSetFeatures(pathfeatures)

        #stock in processed.csv
        #sensitivPenDataSet.stockProcessedData(sensitivPenDataSet.filepath + "_treated_" + sensitivPenDataSet.name + ".csv")

        #display
        #sensitivPenDataSet.DispProcessedData()
        #sensitivPenDataSet.DispRawData()
        sensitivPenDataSet.DispOnlyPenAngles()


if toVisualize:
    """
    """




