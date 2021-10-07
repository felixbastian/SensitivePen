import pandas as pd
import numpy as np

class SensitivePenDataSet():
    """Class that represent a data set of the sensitiv pen.

    """
    def __init__(self, filepath):
        """
        Constructor of the sensitivePen
        :param filepath: filepath of the raw data set
        :param nbPointfilter: level of filtering for the datamanage
        """
        self.name = "SensitivePen"

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")
        self.processedData = self.rawData.copy()

        self.time = []

        # basic data from the movuino
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        # pressure
        self.pressure = self.rawData["pressure"]

        # norm of
        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        # basic data filtered
        self.acceleration_lp = []
        self.gyroscope_lp = []
        self.magnetometer_lp = []

        # time list in seconds
        self.time = list(self.rawData["time"] * 0.001)
        self.rawData["time"] = self.time
        self.processedData["time"] = self.time
        # sample rate
        self.Te = (self.time[-1] - self.time[0]) / (len(self.time))

        # number of row
        self.nb_row = len(self.time)

        # ------ STOCK COLUMN OF DF IN VARIABLES ------
        for k in range(self.nb_row):  # We stock rawData in variables
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]]) * 180 / np.pi)
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            # Calculation of the norm
            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))
            self.normMagnetometer.append(np.linalg.norm(self.magnetometer[k]))

        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)

        # Relevant angle for the pen
        self.sensitivePenAngles = []

        self.posAngAcc = []
        self.initEulerAngles = []
        self.eulerAngles = []

    @staticmethod
    def MovuinoExtraction(serialPort, path):
        isReading = False
        ExtractionCompleted = False
        print("-> Opening serial port {}".format(serialPort))
        arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
        line_byte = ''
        line_str = ''
        datafile = ''
        nbRecord = 1

        while ExtractionCompleted != True:
            line_byte = arduino.readline()
            line_str = line_byte.decode("utf-8")

            if "XXX_end" in line_str and isReading == True :
                isReading = False
                ExtractionCompleted = True
                print("End of data sheet")

                with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                    print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                    file.write(datafile)

            if "XXX_newRecord" in line_str and isReading == True :

                with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                    print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
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




