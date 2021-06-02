import threading
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from scipy import signal
import math
import time

class MovuinoDataSet():

    def __init__(self, filepath):

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")

        print(filepath)

        self.time = []

        # liste de vecteurs numpy
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        self.acceleration_pb = []
        self.acceleration_lp = []
        self.gyroscope_lp = []
        self.magnetometer_lp = []

        self.gravity = []

        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.ThetaGyr = [np.array([0, 0, 0])]
        self.posAngAcc = []

        self.velocity_filter = [np.array([0, 0, 0])]
        self.pos_filter = [np.array([0, 0, 0])]
        self.posAngGyr_filter_lp = [np.array([0, 0, 0])]
        self.posAngAcc_filter = []

        self.time = list(self.rawData["time"]*0.001)
        self.rawData["time"] = self.time

        self.Te = (self.time[-1]-self.time[0])/(len(self.time))

        self.nb_line = len(self.time)

        self.compteur_line = 0

        posAngX = 0
        posAngY = 0
        posAngZ = 0

        posX = 0
        posY = 0
        posZ = 0

        vx = 0
        vy = 0
        vz = 0

    def run(self):
        for k in range(self.nb_line):
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]])*180/np.pi)
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))

        self.velocity = self.EulerIntegration(self.acceleration)
        self.ThetaGyr = self.EulerIntegration(self.gyroscope)
        self.pos = self.EulerIntegration(self.velocity)

        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)

        self.ThetaGyr = np.array(self.ThetaGyr)
        self.pos = np.array(self.pos)
        self.velocity = np.array(self.velocity)

        self.rawData["normAccel"] = self.normAcceleration
        self.rawData["normGyr"] = self.normGyroscope
        self.rawData["ThetaGyrx"] = self.ThetaGyr[:, 0]
        self.rawData["ThetaGyry"] = self.ThetaGyr[:, 1]
        self.rawData["ThetaGyrz"] = self.ThetaGyr[:, 2]

        #--- Gravity recuperation----
        gx = LowPassFilter(self.time, self.acceleration[:, 0], self.Te, 0.0001)
        gy = LowPassFilter(self.time, self.acceleration[:, 1],  self.Te, 0.0001)
        gz = LowPassFilter(self.time, self.acceleration[:, 2],  self.Te, 0.0001)

        for k in range(self.nb_line):
            self.gravity.append(np.array([gx[k], gy[k], gz[k]]))
        self.gravity = np.array(self.gravity)

        #--------------------------- FILTER ----------------------------------

        ax_pb = BandPassButterworthFilter(3, [0.01, 0.5], self.acceleration[:, 0])
        ay_pb = BandPassButterworthFilter(3, [0.01, 0.5], self.acceleration[:, 1])
        az_pb = BandPassButterworthFilter(3, [0.01, 0.5], self.acceleration[:, 2])

        gx_lp = LowPassFilter(self.time, self.gyroscope[:, 0], self.Te, 1)
        gy_lp = LowPassFilter(self.time, self.gyroscope[:, 1], self.Te, 1)
        gz_lp = LowPassFilter(self.time, self.gyroscope[:, 2], self.Te, 1)
        """
        gx_lp = LowPassButterworthFilter(3, 0.1, self.gyroscope[:, 0])
        gy_lp = LowPassButterworthFilter(3, 0.1, self.gyroscope[:, 1])
        gz_lp = LowPassButterworthFilter(3, 0.1, self.gyroscope[:, 2])
        
        gx_lp = self.FiltreNBPointAverage(10, self.gyroscope[:, 0])
        gy_lp = self.FiltreNBPointAverage(10, self.gyroscope[:, 1])
        gz_lp = self.FiltreNBPointAverage(10, self.gyroscope[:, 2])
        """
        self.acceleration_pb = self.acceleration - self.gravity

        for k in range(self.nb_line):
            #self.acceleration_pb.append(np.array([ax_pb[k], ay_pb[k], az_pb[k]]))
            self.gyroscope_lp.append(np.array([gx_lp[k], gy_lp[k], gz_lp[k]]))

        self.posAngGyr_filter_lp = self.EulerIntegration(self.gyroscope_lp)
        self.velocity_filter = self.EulerIntegration(self.acceleration_pb)

        self.acceleration_pb = np.array(self.acceleration_pb)
        self.gyroscope_lp = np.array(self.gyroscope_lp)
        self.posAngGyr_filter_lp = np.array(self.posAngGyr_filter_lp)

        self.velocity_filter = np.array(self.velocity_filter)
        self.StockIntoNewFile(self.filepath)
        self.PlotImage()

    def ConvertArray(*args):

        for arg in args:
            arg = np.array(arg)

    def EulerIntegration(self, Uprime):
        U = [np.array([0, 0, 0])]
        for k in range(self.nb_line-1):
            pas = self.time[k + 1] - self.time[k]

            Ux = Uprime[k][0] * pas + U[k][0]
            Uy = Uprime[k][1] * pas + U[k][1]
            Uz = Uprime[k][2] * pas + U[k][2]
            U.append(np.array([Ux, Uy, Uz]))
        return U


    def FiltreNBPointAverage(self, nb_point, sig): #TODO
        array_to_moy = []
        compteur = 0
        sig_filtre = []

        def moyenne(liste):
            r = 0
            for nb in liste:
                r+= nb
            return r/len(liste)

        for k in range(len(sig)):
            array_to_moy.append(sig[k])
            if (len(array_to_moy) >= nb_point) :
                sig_filtre.append(moyenne(array_to_moy[k+1-nb_point:k+1]))
            else:
                sig_filtre.append(moyenne(array_to_moy))

        return sig_filtre

    def StockIntoNewFile(self, filepath):
        self.rawData.to_csv(filepath + "_treated" + ".csv", sep=",", index=False, index_label=False)

    def PlotImage(self):

        a = plt.subplot(331)
        a.plot(self.time, self.acceleration[:, 0], color="red")
        a.plot(self.time, self.acceleration[:, 1], color="green")
        a.plot(self.time, self.acceleration[:, 2], color="blue")
        a.set_title('Acceleration (m/s2)')

        g = plt.subplot(332)
        g.plot(self.time, self.gyroscope[:, 0], color="r")
        g.plot(self.time, self.gyroscope[:, 1], color="green")
        g.plot(self.time, self.gyroscope[:, 2], color="blue", marker=".")
        g.set_title('Gyroscope (deg/s)')

        m = plt.subplot(333)
        m.plot(self.time, self.magnetometer[:, 0], color="r")
        m.plot(self.time, self.magnetometer[:, 1], color="green")
        m.plot(self.time, self.magnetometer[:, 2], color="blue")
        m.set_title('Magnetometre')

        v = plt.subplot(334)
        v.plot(self.time, self.velocity[:, 0], color="r")
        v.plot(self.time, self.velocity[:, 1], color="green")
        v.plot(self.time, self.velocity[:, 2], color="blue")
        v.set_title('Velocity (m/s)')
        
        theta = plt.subplot(335)
        theta.plot(self.time, self.ThetaGyr[:, 0], color="r")
        theta.plot(self.time, self.ThetaGyr[:, 1], color="green")
        theta.plot(self.time, self.ThetaGyr[:, 2], color="blue")
        theta.set_title('Angle (deg)')

        accel_pb = plt.subplot(336)
        accel_pb.plot(self.time, self.acceleration_pb[:, 0], color="r")
        accel_pb.plot(self.time, self.acceleration_pb[:, 1], color="green")
        accel_pb.plot(self.time, self.acceleration_pb[:, 2], color="blue")
        accel_pb.set_title('Acceleration Passe bande')

        velocity_pb = plt.subplot(337)
        velocity_pb.plot(self.time, self.velocity_filter[:, 0], color="r")
        velocity_pb.plot(self.time, self.velocity_filter[:, 1], color="green")
        velocity_pb.plot(self.time, self.velocity_filter[:, 2], color="blue")
        velocity_pb.set_title('Velocity Passe bande')

        omega_lp = plt.subplot(338)
        omega_lp.plot(self.time, self.gyroscope_lp[:, 0], color="r")
        omega_lp.plot(self.time, self.gyroscope_lp[:, 1], color="green")
        omega_lp.plot(self.time, self.gyroscope_lp[:, 2], color="blue")
        omega_lp.set_title('Gyroscope Passe bas deg/s')

        theta_lp = plt.subplot(339)
        theta_lp.plot(self.time, self.posAngGyr_filter_lp[:, 0], color="r")
        theta_lp.plot(self.time, self.posAngGyr_filter_lp[:, 1], color="green")
        theta_lp.plot(self.time, self.posAngGyr_filter_lp[:, 2], color="blue")
        theta_lp.set_title('Angle filtré (deg)')

        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="center right", bbox_to_anchor=(-2.5,3.6),ncol=1)
        plt.show()

    def TrapezeIntegration(self, y1, y2, t1, t2, dt=0):
        return np.trapz([y1, y2], [t1, t2])

    def GetAnglewithAcc(self):
        for k in range(self.nb_line):
            gx = self.acceleration[k, 0]
            gy = self.acceleration[k, 1]
            gz = self.acceleration[k, 2]
            Gxy = np.array([gx, gy])
            Gyz = np.array([gy, gz])
            Gzx = np.array([gz, gx])

            alpha = math.acos(gx / np.linalg.norm(Gxy))
            beta = math.acos(gy / np.linalg.norm(Gyz))
            gamma = math.acos(gz / np.linalg.norm(Gzx))

            angle = np.array([beta, alpha, gamma]) * 360 / (2 * np.pi)

            self.posAngAcc.append(angle)
            print(angle)
        self.posAngAcc = np.array(self.posAngAcc)

def LowPassFilter(x, y, Te, fc):
    """

    :param x: Absice
    :param y: Signal to filter
    :param Te: Periode d'écanhtillonage
    :param fc: Frequnce de coupure
    :return: signal filtre
    """
    tau = 1/(2*np.pi*fc)
    y_lp = [y[0]]
    for i in range(len(x)-1):
        y_lp.append(y_lp[i] + Te/tau * (y[i] - y_lp[i]))
    return y_lp

def LowPassButterworthFilter(b,a, sig):
    b,a = signal.butter(b,a)
    sig_filtre = signal.filtfilt(b,a, sig)
    return sig_filtre

def BandPassButterworthFilter(order,cutsLim,sig):
    b,a = signal.butter(order,cutsLim,btype = "bandpass")
    sig_filter = signal.filtfilt(b,a, sig)
    return sig_filter

def BandPassFilter():
    return 0

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs  # sampling frequency
    low = lowcut / nyq
    high = highcut / nyq
    sos = signal.butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos


def butter_bandpass_filter(sig, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    sig_filtered = signal.sosfilt(sos, sig)
    return sig_filtered
"""
class MovuinoDataSetThread(Thread):

    def __init__(self, filepath):

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")

        self.time = []

        # liste de vecteurs numpy
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        self.velocity = [np.array([0, 0, 0])]
        self.pos = [np.array([0, 0, 0])]
        self.posAng = [np.array([0, 0, 0])]

        posAngX = 0
        posAngY = 0
        posAngZ = 0

        posX = 0
        posY = 0
        posZ = 0

        vx = 0
        vy = 0
        vz = 0

        self.time = list(self.rawData["time"])

        self.nb_line = len(self.time)

        self.compteur_line = 0
        self.thread = Thread.__init__(self)

    def run(self):
        for k in range(self.nb_line):
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]]))
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))

            #---- integration -----
            if k < self.nb_line-1:
                pas = self.time[k+1] - self.time[k]

                posAngX = self.gyroscope[k][0]*pas*0.001*180/np.pi + self.posAng[k][0]  # 360/2np.pi
                posAngY = self.gyroscope[k][1]*pas*0.001*180/np.pi + self.posAng[k][1]
                posAngZ = self.gyroscope[k][2]*pas*0.001*180/np.pi + self.posAng[k][2]
                self.posAng.append(np.array([posAngX, posAngY, posAngZ]))

                vx = self.acceleration[k][0]*pas*0.001*180/np.pi + self.velocity[k][0]  # 360/2np.pi
                vy = self.acceleration[k][1]*pas*0.001*180/np.pi + self.velocity[k][1]
                vz = self.acceleration[k][2]*pas*0.001*180/np.pi + self.velocity[k][2]
                self.posAng.append(np.array([vx, vy, vz]))

                posX = self.velocity[k][0]*pas*0.001*180/np.pi + self.posX[k][0]  # 360/2np.pi
                posY = self.velocity[k][1]*pas*0.001*180/np.pi + self.posY[k][1]
                posZ = self.velocity[k][2]*pas*0.001*180/np.pi + self.posZ[k][2]
                self.pos.append(np.array([posX, posY, posZ]))



            if k == self.nb_line-1:
                self.ConvertArray()
                self.StockIntoNewFile()
                self.plotImage()

    def ConvertArray(self):
        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)

        self.posAng = np.array(self.posAng)
        self.pos = np.array(self.pos)
        self.velocity = np.array(self.velocity)

        self.rawData["normAccel"] = self.normAcceleration
        self.rawData["normGyr"] = self.normGyroscope

    def StockIntoNewFile(self):
        self.rawData.to_csv(self.filepath + "_treated" + ".csv", sep=",", index=False, index_label=False)

    def plotImage(self):

        a = plt.subplot(331)

        a.plot(self.time, self.acceleration[:, 0], color = "r")
        a.plot(self.time, self.acceleration[:, 1], color = "green")
        a.plot(self.time, self.acceleration[:, 2], color = "blue")
        g.set_title('Acceleration')

        g = plt.subplot(332)
        g.plot(self.time, self.self.gyroscope[:, 0], color="r")
        g.plot(self.time, self.self.gyroscope[:, 1], color="green")
        g.plot(self.time, self.self.gyroscope[:, 2], color="blue")
        g.set_title('Gyroscope')
        plt.show()

    def TrapezeIntegration(self, y1, y2, t1, t2, dt=0):
        return np.trapz([y1, y2], [t1, t2])
"""