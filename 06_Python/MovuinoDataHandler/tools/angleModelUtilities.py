import numpy as np

def LinearReg(angleData):

    nbpts = len(angleData)
    x = np.linspace(0, 1, nbpts)
    X = np.vstack([x, np.ones(len(x))]).T
    # X = [[x1, 1],
    #      [x2, 1],
    #      ...
    #      [xn, 1]]
    resultat = np.linalg.lstsq(X, angleData, rcond=None)

    aopt, bopt = resultat[0]
    erreur = resultat[1][0] / nbpts

    reg = [aopt * i + bopt for i in x]
    return aopt, bopt, erreur, reg