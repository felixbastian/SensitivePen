import threading
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
import tools.GetAngleMethods as gam
import tools.DisplayFunctions as df
from scipy import signal
from scipy.spatial.transform import Rotation as R
import math
import sys
import time


class MovuinoDataSet():

    def __init__(self, filepath):
        """
        Get the data from the file (.csv) ad initialize global variables.


        :param filepath: Where the file is stocked.
        :param nbPointfilter: You can choose the quality/amount of filtration of the data
        """

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")

        self.time = []

        # basic data from the movuino
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        # time list in seconds
        self.time = list(self.rawData["time"]*0.001)
        self.rawData["time"] = self.time

        # sample rate
        self.Te = (self.time[-1]-self.time[0])/(len(self.time))

        # number of row
        self.nb_row = len(self.time)

        #------ STOCK COLUMN OF DF IN VARIABLES ------
        for k in range(self.nb_row): #We stock rawData in variables
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]])*180/np.pi)
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)