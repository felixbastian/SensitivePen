import dataSet.SensitivePenDataSet as sp
import numpy as np

import matplotlib.pyplot as plt

############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\Data_Elderly\\02_treated_data\\"
filename = "F20D_sentence_treated_SensitivePen.csv"
sep = ","
decimal = "."


stationnarity_interval = (7, 38)  #Intervalle en sec

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
line_interval = (6,27.5)
index_line_init = int(line_interval[0] * 1/Te)
index_line_end = int(line_interval[1]*1/Te)

line_psi = sensitivPenDataSet.sensitivePenAngles[index_line_init:index_line_end, 0]
nbpts = len(line_psi)
x = np.linspace(0, 1, nbpts)
X = np.vstack([x, np.ones(len(x))]).T
# X = [[x1, 1],
#      [x2, 1],
#      ...
#      [xn, 1]]
resultat = np.linalg.lstsq(X, line_psi,rcond=None)

aopt, bopt = resultat[0]
erreur = resultat[1][0]/nbpts

line_psi_estimated = [aopt*i+bopt for i in x]

plt.plot(x, line_psi, "b+") # nuage de points
plt.plot(x, line_psi_estimated,"r") # droite de régression
plt.show()

print("a =", aopt.round(2), ", b =", bopt.round(2),"; χ² =", erreur.round(2))












