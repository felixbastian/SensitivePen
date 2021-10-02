import numpy as np

def stockProcessedData(sensitivPen, filepath):
    """

    :param sensitivPen:
    :param folderpath:
    :return:
    """

    sensitivPen.processedData = sensitivPen.rawData.copy()

    sensitivPen.processedData["normAccel"] = sensitivPen.normAcceleration
    sensitivPen.processedData["normMag"] = sensitivPen.normMagnetometer
    sensitivPen.processedData["normGyr"] = sensitivPen.normGyroscope

    sensitivPen.processedData["ax_filter"] = sensitivPen.acceleration_lp[:,0]
    sensitivPen.processedData["ay_filter"] = sensitivPen.acceleration_lp[:,1]
    sensitivPen.processedData["az_filter"] = sensitivPen.acceleration_lp[:,2]

    sensitivPen.processedData["gx_filter"] = sensitivPen.gyroscope_lp[:,0] * 180 / np.pi
    sensitivPen.processedData["gy_filter"] = sensitivPen.gyroscope_lp[:,1] * 180 / np.pi
    sensitivPen.processedData["gz_filter"] = sensitivPen.gyroscope_lp[:,2] * 180 / np.pi

    sensitivPen.processedData["mx_filter"] = sensitivPen.magnetometer_lp[:,0]
    sensitivPen.processedData["my_filter"] = sensitivPen.magnetometer_lp[:,1]
    sensitivPen.processedData["mz_filter"] = sensitivPen.magnetometer_lp[:,2]

    sensitivPen.processedData["psi"] = sensitivPen.sensitivePenAngles[:, 0]
    sensitivPen.processedData["theta"] = sensitivPen.sensitivePenAngles[:, 1]

    sensitivPen.processedData.to_csv(filepath, sep=",", index=False, index_label=False)