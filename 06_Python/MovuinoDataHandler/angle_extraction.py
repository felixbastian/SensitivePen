import dataSet.SensitivePenDataSet as sp
import tools.angleModelUtilities as amu
import numpy as np

import matplotlib.pyplot as plt

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\Data_Elderly\\"
filename = "M20F_loops_treated_SensitivePen.csv"
sep = ","
decimal = "."


stationnarity_interval = (3000,26000) #Intervalle en sec

###################################

# -------- Data processing ----------------------

sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
Te = sensitivPenDataSet.Te
print("sample frequency : " + str(1 / Te))

index_init = int(stationnarity_interval[0] * 1/Te)
index_end = int(stationnarity_interval[1]*1/Te)

stationary_psi = sensitivPenDataSet.sensitivePenAngles[index_init:index_end, 0]
stationary_theta = sensitivPenDataSet.sensitivePenAngles[index_init:index_end, 1]

#Statistics calcul for psi and theta

#Moyenne variance
mean_psi = np.mean(stationary_psi)
mean_theta = np.mean(stationary_theta)

sig_psi = np.std(stationary_psi)
sig_theta = np.std(stationary_theta)
print(index_init)
print(index_end)
print("Psi : -> mean : {}, -> sigma : {}".format(mean_psi, sig_psi))
print("Theta : -> mean : {}, -> sigma : {}".format(mean_theta, sig_theta))

sensitivPenDataSet.DispOnlyPenAngles()

#Regression :

line_interval = (3000,26000) #secondes
index_line_init = int(line_interval[0] * 1/Te)
index_line_end = int(line_interval[1]*1/Te)

line_psi = sensitivPenDataSet.psi[index_line_init:index_line_end]
line_theta = sensitivPenDataSet.theta[index_line_init:index_line_end]

x = np.linspace(0, 1, len(line_psi))

a_psi, b_psi, er_psi, reg_psi = amu .LinearReg(line_psi)
a_theta, b_theta, er_theta, reg_theta = amu .LinearReg(line_theta)

print("a =", a_psi.round(2), ", b =", b_psi.round(2),"; χ² =", er_psi.round(2))
plt.plot(x, line_psi, "b-+") # nuage de points
plt.plot(x, reg_psi,"r") # droite de régression
plt.title("Psi = f(pourcentage d'avancement de la ligne)")
plt.show()

print("a =", a_theta.round(2), ", b =", b_theta.round(2),"; χ² =", er_theta.round(2))
plt.plot(x, line_theta, "b-+") # nuage de points
plt.plot(x, reg_theta,"r") # droite de régression
plt.title("Psi = f(pourcentage d'avancement de la ligne)")
plt.show()














