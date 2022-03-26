import pandas as pd
import math
import numpy as np

def calculateTip(df):
    lengthOfPen = 0.1

    #The difference between the top (where data gets collected) and the tip (where the ink comes out) is relative to the length of the pen
    #When only looking at the translation, the tip and the top move the same in the coordinate system -> accX, accY, accZ
    #When only looking at the rotation of the pen, we have to account for relative location changes that are dependent on the length of the pen


    translationAdjustment = [df['accX_Top'], df['accY_Top'], df['accZ_Top']]
    rotationAdjustment = [2*(np.cos(df['psi'])*np.cos(df['theta'])-(np.sin(df['psi'])*np.sin(df['theta']))),
                        2*(np.sin(df['psi'])*np.cos(df['theta'])+(np.cos(df['psi'])*np.sin(df['theta']))),
                        np.sin(df['theta'])]


    #Looking at the translation and rotation together:
    #Formula = TranslationAdjusment + length*rotationAdjustment
    translatedDF = pd.DataFrame(np.add(lengthOfPen*np.array(rotationAdjustment),translationAdjustment))
    translatedDF = translatedDF.rename(index={0: "accX_Tip", 1: "accY_Tip", 2: "accZ_Tip"})

    return translatedDF.T