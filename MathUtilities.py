import numpy as np
import pandas as pd


def integral(df,data):
    integral = [0]
    for i in range(len(df.index) - 1):
            dt_ = df.time[i + 1] - df.time[i]
            integral_ = data[i] * dt_
            integral_ += (data[i + 1] - data[i]) * dt_ / 2.0
            integral.append(integral[i] + integral_)
    return(integral)

def derivData(df,data):
    derivData = [0]
    for i in range(len(df.index) - 1):
        if i == 0:
            derivData.append((data[i + 1] - data[i]) / (df.time[i + 1] - df.time[i]))
        elif i == len(df.index) - 1:
            derivData.append((data[i] - data[i - 1]) / (df.time[i] - df.time[i - 1]))
        else:
            derivData.append((data[i + 1] - data[i - 1]) / (df.time[i + 1] - df.time[i - 1]))
    return(derivData)

def angle(df,X,Z):
    angle = [0]
    angle = np.arctan(X/Z)
    return(angle)

def norme(df):
    norme = np.sqrt(((df['accX'])**2)+(df['accY']**2)+(df['accZ']**2))
    return(norme)


