import dataSet.SensitivePenDataSet as sp
import numpy as np

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\Data_Elderly\\02_treated_data\\"
filename = "M20F_sentence_treated_SensitivePen.csv"
sep = ","
decimal = "."


stationnarity_interval = (8, 36)  #Intervalle en sec

###################################

# -------- Data processing ----------------------

sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
Te = sensitivPenDataSet.Te
print("sample frequency : " + str(1 / Te))

index_init = int(stationnarity_interval[0] * 1/Te)
index_end = int(stationnarity_interval[1]*1/Te)

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









