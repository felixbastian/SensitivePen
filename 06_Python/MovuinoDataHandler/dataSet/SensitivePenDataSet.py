import pandas as pd
import numpy as np
import serial
import tools.DisplayFunctions as df
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
import tools.GetAngleMethods as gam
import os

import math

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
        self.filename = os.path.basename(self.filepath)
        print("Reading : " + filepath)
        self.rawData = pd.read_csv(filepath, sep=",")
        self.processedData = self.rawData.copy()

        self.time = []

        # basic data from the movuino
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        # pressure
        self.pressure = self.rawData["pressure"]
        self.pressure = np.array(self.pressure)

        # norm of
        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        # norm filtered of
        self.normAcceleration_lp = []
        self.normGyroscope_lp = []
        self.normMagnetometer_lp = []

        # basic data filtered
        self.acceleration_lp = []
        self.gyroscope_lp = []
        self.magnetometer_lp = []

        # time list in seconds
        if "treated" in self.filename:
            self.time = list(self.rawData["time"])
        else:
            self.time = list(self.rawData["time"] * 0.001)
        self.rawData["time"] = self.time
        self.processedData["time"] = self.time
        # sample rate
        self.Te = (self.time[-1] - self.time[0]) / (len(self.time))

        # number of row
        self.nb_row = len(self.time)

        # Relevant angle for the pen
        self.sensitivePenAngles = []

        self.posAngAcc = []
        self.initEulerAngles = []
        self.eulerAngles = []


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

        if "treated" in self.filename:
            for k in range(self.nb_row):  # We stock rawData in variables
                self.acceleration_lp.append(np.array([self.rawData["ax_filter"][k], self.rawData["ay_filter"][k], self.rawData["az_filter"][k]]))
                self.gyroscope_lp.append(np.array([self.rawData["gx_filter"][k], self.rawData["gy_filter"][k], self.rawData["gz_filter"][k]]) * 180 / np.pi)
                self.magnetometer_lp.append(np.array([self.rawData["mx_filter"][k], self.rawData["my_filter"][k], self.rawData["mz_filter"][k]]))

                # Calculation of the norm
                self.normAcceleration_lp.append(np.linalg.norm(self.acceleration_lp[k]))
                self.normGyroscope_lp.append(np.linalg.norm(self.gyroscope_lp[k]))
                self.normMagnetometer_lp.append(np.linalg.norm(self.magnetometer_lp[k]))

                self.sensitivePenAngles.append(np.array([self.rawData["psi"][k], self.rawData["theta"][k]]))

            self.acceleration_lp = np.array(self.acceleration_lp)
            self.gyroscope_lp = np.array(self.gyroscope_lp)
            self.normMagnetometer_lp = np.array(self.magnetometer_lp)
            self.sensitivePenAngles = np.array(self.sensitivePenAngles)



    def computePenAngles(self):
        """
        Calculate psi and theta angle given the accekeration and the magnetometer of the pen

        :param self:
        :return:
        """
        # --- Getting initial euler angles
        initRotationMatrix = gam.rotationMatrixCreation(self.acceleration_lp[15], self.magnetometer[15])
        self.initPsi = math.atan2(initRotationMatrix[0, 1], initRotationMatrix[0, 0])

        for k in range(len(self.time)):
            # --- Getting rotation matrix from filtered data
            rotationMatrix = gam.rotationMatrixCreation(self.acceleration_lp[k], self.magnetometer[k])

            # --- Get inclinaison of the pen (theta)
            self.posAngAcc.append(gam.getInclinaison(self.acceleration_lp[k]))
            theta = self.posAngAcc[k][0] - 90

            # --- getting orientation of the pen (for psi)
            a00 = rotationMatrix[0, 0]  # N.x
            a01 = rotationMatrix[0, 1]  # E.x

            if (abs(theta) > 360):  # set the lim to 80 but not usefull now
                psi = 0
            else:
                psi = (math.atan2(a01, a00) - self.initPsi) * 180 / math.pi

                if -180 > psi >= -360:
                    psi += 360
                elif 180 < psi <= 360:
                    psi -= 360

            self.sensitivePenAngles.append(np.array([psi, theta]))

        self.posAngAcc = np.array(self.posAngAcc)
        self.sensitivePenAngles = np.array(self.sensitivePenAngles)

        return self.sensitivePenAngles

    def stockProcessedData(self, filepath):
        """

        :param self:
        :param folderpath:
        :return:
        """
        dir = os.path.dirname(filepath)
        if not os.path.exists(os.path.dirname(filepath)) :
            os.makedirs(dir)
        self.processedData["normAccel"] = self.normAcceleration
        self.processedData["normMag"] = self.normMagnetometer
        self.processedData["normGyr"] = self.normGyroscope

        self.processedData["ax_filter"] = self.acceleration_lp[:, 0]
        self.processedData["ay_filter"] = self.acceleration_lp[:, 1]
        self.processedData["az_filter"] = self.acceleration_lp[:, 2]

        self.processedData["gx_filter"] = self.gyroscope_lp[:, 0] * 180 / np.pi
        self.processedData["gy_filter"] = self.gyroscope_lp[:, 1] * 180 / np.pi
        self.processedData["gz_filter"] = self.gyroscope_lp[:, 2] * 180 / np.pi

        self.processedData["mx_filter"] = self.magnetometer_lp[:, 0]
        self.processedData["my_filter"] = self.magnetometer_lp[:, 1]
        self.processedData["mz_filter"] = self.magnetometer_lp[:, 2]

        self.processedData["psi"] = self.sensitivePenAngles[:, 0]
        self.processedData["theta"] = self.sensitivePenAngles[:, 1]

        self.processedData.to_csv(filepath, sep=",", index=False, index_label=False)

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

    def DispRawData(self):
        time_list = self.time
        df.PlotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 221)
        df.PlotVector(time_list, self.magnetometer, 'Magnetometer', 222)
        df.PlotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 223)

        pressure = plt.subplot(224)
        pressure.plot(time_list, self.pressure)
        pressure.set_title('Pressure (pressure unit)')
        plt.show()

    def DispProcessedData(self):

        time_list = self.processedData["time"]
        df.PlotVector(time_list, self.acceleration, 'Acceleration (m/s2)', 331)
        df.PlotVector(time_list, self.magnetometer, 'Magnetometer', 332)
        df.PlotVector(time_list, self.gyroscope, 'Gyroscope (deg/s)', 333)
        df.PlotVector(time_list, self.acceleration_lp, 'Acceleration filtered (LP)', 334)
        df.PlotVector(time_list, self.magnetometer_lp, 'Magnetometer filtered (LP)', 335)

        normMag = plt.subplot(338)
        normMag.plot(time_list, self.normMagnetometer, color="black")
        normMag.set_title("Norm Magnetometer")

        normAcc = plt.subplot(337)
        normAcc.plot(time_list, self.normAcceleration, color="black")
        normAcc.set_title("Norm Acceleration")

        pressure = plt.subplot(339)
        pressure.plot(time_list, self.pressure)
        pressure.set_title('Pressure (pressure unit)')

        sensitivePenAngle = plt.subplot(336)
        sensitivePenAngle.plot(time_list, self.sensitivePenAngles[:, 0], color="red", label='psi')
        sensitivePenAngle.plot(time_list, self.sensitivePenAngles[:, 1], color="blue", label='theta')
        sensitivePenAngle.grid(b=True, which='major')
        sensitivePenAngle.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        sensitivePenAngle.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        sensitivePenAngle.minorticks_on()
        sensitivePenAngle.set_yticks([-180, -90, 0, 90, 180])
        sensitivePenAngle.set_ylim(-220, 220)
        sensitivePenAngle.yaxis.set_minor_locator(MultipleLocator(45))
        sensitivePenAngle.legend(loc='upper right')
        sensitivePenAngle.set_title("Relevant angle (psi, theta) (deg)")

        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="upper right", bbox_to_anchor=(2.5, 3.6), ncol=1)
        plt.title(os.path.basename(self.filepath))
        plt.show()

    def DispOnlyPenAngles(self):
        print("Plotting : {}".format(os.path.basename(self.filepath)))
        timeList = self.processedData["time"]

        psi = self.processedData["psi"]
        theta = self.processedData["theta"]

        accel = df.PlotVector(timeList, self.acceleration, "Acceleration m/s2", 221)
        accel.plot(timeList, self.normAcceleration_lp, color="black", label = "norm")
        accel.legend(loc="upper right")

        df.PlotVector(timeList, self.gyroscope, "Gyroscope m/s", 222)

        mag = df.PlotVector(timeList, self.magnetometer, "Magnetometer unit mag", 223)
        mag.plot(timeList, self.normMagnetometer, color="black", label = "norm")
        mag.legend(loc="upper right")

        sensitivePenAngle = plt.subplot(224)
        sensitivePenAngle.plot(timeList, psi, color="red", label='psi')
        sensitivePenAngle.plot(timeList, theta, color="blue", label='theta')
        sensitivePenAngle.grid(b=True, which='major')
        sensitivePenAngle.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        sensitivePenAngle.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        sensitivePenAngle.minorticks_on()
        sensitivePenAngle.set_yticks([-180, -90, 0, 90, 180])
        sensitivePenAngle.yaxis.set_minor_locator(MultipleLocator(45))
        sensitivePenAngle.legend(loc='upper right')
        sensitivePenAngle.set_title("Relevant angle (psi, theta) (deg)")

        plt.title(os.path.basename(self.filepath))
        plt.show()




