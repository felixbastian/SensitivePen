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
    """
    Mother class for every data that comes out from the movuino.
    It manages the data in order to process it after.
    In this class only basic operations are done : filtration and norm

    -> Attributs :
    * filepath : dataset filepath
    * rawData : dataframe containing the dataset
    * nbPointFilter : level of filtering
    * time : time list of the rawData
    * Te : sample rate
    * nb_row : number of line in rawData

    * acceleration : acceleration list
    * gyroscope : gyroscope list
    * magnetometer : magnetometer list

    * listMeanAcc : acceleration list usefull for data filtering
    * listMeanGyr : gyroscope list usefull for data filtering
    * listMeanMag : magnetometer list usefull for data filtering

    * acceleration_lp : acceleration filtered list
    * gyroscope_lp : gyroscope filtered list
    * magnetometer_lp : magnetometer filtered list

    * normAcceleration : list of norm acceleration
    * normGyroscope : list of norm gyroscope
    * normMagnetometer : list of norm magnetometer

    -> Methods :
    * __init(filepath, nbPointFilter) : constructor
    * DataManage : Processes the data
    * StockIntoNewFile : stock the data into a new file
    * VisualizeData : Visualize data
    * PlotImage : Put into subplot differents variables
    * AddingRawData : Add rows in the rawData
    * PlotCompleteFile (@static) : Show a complete file whithout processing data
    """
    def __init__(self, filepath):
        """
        Get the data from the file (.csv) ad initialize global variables.


        :param filepath: Where the file is stocked.
        :param nbPointfilter: You can choose the quality/amount of filtration of the data
        """

        self.filepath = filepath
        self.rawData = pd.read_csv(filepath + ".csv", sep=",")
        self.processedData = pd.DataFrame()
        self.featuredData = ''

        self.time = []

        # basic data from the movuino
        self.acceleration = []
        self.gyroscope = []
        self.magnetometer = []

        # Usefull for the filtration
        self.listMeanAcc = []
        self.listMeanGyr = []
        self.listMeanMag = []

        # basic data filtered
        self.acceleration_lp = []
        self.gyroscope_lp = []
        self.magnetometer_lp = []

        # norm of
        self.normAcceleration = []
        self.normGyroscope = []
        self.normMagnetometer = []

        self.normAcceleration_lp = []
        self.normGyroscope_lp = []
        self.normMagnetometer_lp = []

        # time list in seconds
        self.time = list(self.rawData["time"]*0.001)
        self.rawData["time"] = self.time
        self.processedData = self.rawData.copy()

        # sample rate
        self.Te = (self.time[-1]-self.time[0])/(len(self.time))

        # number of row
        self.nb_row = len(self.time)

        #------ STOCK COLUMN OF DF IN VARIABLES ------
        for k in range(self.nb_row): #We stock rawData in variables
            self.acceleration.append(np.array([self.rawData["ax"][k], self.rawData["ay"][k], self.rawData["az"][k]]))
            self.gyroscope.append(np.array([self.rawData["gx"][k], self.rawData["gy"][k], self.rawData["gz"][k]])*180/np.pi)
            self.magnetometer.append(np.array([self.rawData["mx"][k], self.rawData["my"][k], self.rawData["mz"][k]]))

            #Calculation of the norm
            self.normAcceleration.append(np.linalg.norm(self.acceleration[k]))
            self.normGyroscope.append(np.linalg.norm(self.gyroscope[k]))
            self.normMagnetometer.append(np.linalg.norm(self.magnetometer[k]))

        self.acceleration = np.array(self.acceleration)
        self.gyroscope = np.array(self.gyroscope)
        self.magnetometer = np.array(self.magnetometer)