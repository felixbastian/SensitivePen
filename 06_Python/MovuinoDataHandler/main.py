import dataSet.SensitivePenDataSet as sp
import tools.FilterMethods as fm
import tools.features_extraction_scripts.runFeature as ft
import os

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\testESP32\\02_treated_data\\"
fileName = "record"  # generic name numbers will be added for duplicates
pathfeatures ="zozo.csv"
serialPort = 'COM4'

toExtract = False
toDataManage = False
toVisualize = True

filter = 20

sep = ","
decimal = "."

"""
# Send read SPIFF instruction to Movuino
    arduino.write(bytes("r", 'ascii'))

"""
###################################

# --------- Data Extraction from Movuino ----------
if toExtract:
    """
    Extract data from the serial port and stock it into a csv file
    """
    print("Data extraction..")
    sp.SensitivePenDataSet.MovuinoExtraction(serialPort, folderPath + fileName)


# -------- Data processing ----------------------

for filename in os.listdir(folderPath):
    print(filename)
    if os.path.basename(filename).endswith("csv"):
        sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
        Te = sensitivPenDataSet.Te
        print("sample frequency : " + str(1/Te))

        if toDataManage:
            #Filtering
            sensitivPenDataSet.acceleration_lp = fm.MeanFilter(sensitivPenDataSet.acceleration, filter)
            sensitivPenDataSet.gyroscope_lp = fm.MeanFilter(sensitivPenDataSet.gyroscope, filter)
            sensitivPenDataSet.magnetometer_lp = fm.MeanFilter(sensitivPenDataSet.magnetometer, filter)

            #ComputeAngles
            sensitivPenDataSet.computePenAngles()

            #FeaturesDifference between runcode et runfeatures extract
            #ft.getDataSetFeatures(pathfeatures)

            #stock in processed.csv
            treated_filepath = os.path.dirname(sensitivPenDataSet.filepath) + "\\02_treated_data\\" + sensitivPenDataSet.filename[:-4] + "_treated_" + sensitivPenDataSet.name + ".csv"
            sensitivPenDataSet.stockProcessedData(treated_filepath)

            if toVisualize:
                # display
                # sensitivPenDataSet.DispProcessedData()
                # sensitivPenDataSet.DispRawData()
                if "treated" in filename:
                    sensitivPenDataSet.DispOnlyPenAngles()


        if toVisualize and not toDataManage:
            # display
            # sensitivPenDataSet.DispProcessedData()
            sensitivPenDataSet.DispRawData()
            if "treated" in filename:
                sensitivPenDataSet.DispOnlyPenAngles()






