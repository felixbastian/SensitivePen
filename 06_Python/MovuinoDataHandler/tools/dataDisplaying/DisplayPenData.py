import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox
from matplotlib.ticker import MultipleLocator
import tools.DisplayFunctions as df

def DispRawData(sensitivPen):
    time_list = sensitivPen.time
    df.PlotVector(time_list, sensitivPen.acceleration, 'Acceleration (m/s2)', 221)
    df.PlotVector(time_list, sensitivPen.magnetometer, 'Magnetometer', 222)
    df.PlotVector(time_list, sensitivPen.gyroscope, 'Gyroscope (deg/s)', 223)

    pressure = plt.subplot(224)
    pressure.plot(time_list, sensitivPen.pressure)
    pressure.set_title('Pressure (pressure unit)')
    plt.show()

def DispProcessedData(sensitivPen):

    time_list =sensitivPen.time
    df.PlotVector(time_list, sensitivPen.acceleration, 'Acceleration (m/s2)', 331)
    df.PlotVector(time_list, sensitivPen.magnetometer, 'Magnetometer', 332)
    df.PlotVector(time_list, sensitivPen.gyroscope, 'Gyroscope (deg/s)', 333)
    df.PlotVector(time_list, sensitivPen.acceleration_lp, 'Acceleration filtered (LP)', 334)
    df.PlotVector(time_list, sensitivPen.magnetometer_lp, 'Magnetometer filtered (LP)', 335)

    normMag = plt.subplot(338)
    normMag.plot(time_list, sensitivPen.normMagnetometer, color="black")
    normMag.set_title("Norm Magnetometer")

    normAcc = plt.subplot(337)
    normAcc.plot(time_list, sensitivPen.normAcceleration, color="black")
    normAcc.set_title("Norm Acceleration")

    pressure = plt.subplot(339)
    pressure.plot(time_list, sensitivPen.pressure)
    pressure.set_title('Pressure (pressure unit)')

    sensitivePenAngle = plt.subplot(336)
    sensitivePenAngle.plot(time_list, sensitivPen.sensitivePenAngles[:, 0], color="red", label='psi')
    sensitivePenAngle.plot(time_list, sensitivPen.sensitivePenAngles[:, 1], color="blue", label='theta')
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

    plt.show()

def DispOnlyPenAngles(sensitivPen):
    timeList = sensitivPen.time
    psi = sensitivPen.sensitivePenAngles[:, 0]
    theta = sensitivPen.sensitivePenAngles[:, 1]

    df.PlotVector(timeList, sensitivPen.acceleration, "Acceleration m/s2", 221)
    df.PlotVector(timeList, sensitivPen.gyroscope, "Gyroscope m/s", 222)

    mag = df.PlotVector(timeList, sensitivPen.magnetometer, "Magnetometer unit mag", 223)
    mag.plot(timeList, sensitivPen.normMagnetometer, color="black")
    mag.legend()

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

    plt.show()