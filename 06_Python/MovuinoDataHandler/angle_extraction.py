import dataSet.SensitivePenDataSet as sp
import tools.FilterMethods as fm
import tools.features_extraction_scripts.runFeature as ft
import os
import numpy as np

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\Data_Postures\\treated_data\\"
filename = "B4_sentence_en_treated_SensitivePen.csv"
sep = ","
decimal = "."


stationnarity_int = (5, 21)

###################################

# -------- Data processing ----------------------

sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
Te = sensitivPenDataSet.Te
print("sample frequency : " + str(1 / Te))

index_init = int(stationnarity_int[0] * 1/Te)
index_end = int(stationnarity_int[1]*1/Te)

stationary_psi = sensitivPenDataSet.sensitivePenAngles[index_init:index_end, 0]
stationary_theta = sensitivPenDataSet.sensitivePenAngles[index_init:index_end, 1]

mean_psi = np.mean(stationary_psi)
mean_theta = np.mean(stationary_theta)

sig_psi = np.std(stationary_psi)
sig_theta = np.std(stationary_theta)
print(index_init)
print(index_end)
print("Psi : -> mean : {}, -> sigma : {}".format(mean_psi, sig_psi))
print("Theta : -> mean : {}, -> sigma : {}".format(mean_theta, sig_theta))

sensitivPenDataSet.DispOnlyPenAngles()









