from math import sqrt
from matplotlib import pyplot as plt


def rmse(row):
    return sqrt((row["y_real"]-row["y_pred"])**2)

def plotPrediction(df):
    print(df)
    df["rmse"] = df.apply(lambda row: rmse(row), axis=1)

    print('RMSE: Mean')
    print(df["rmse"].mean())


    y = df['y_real']
    plt.figure(figsize=(10,8))
    plt.grid()
    plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
    plt.scatter(df.y_real, df.y_pred, c=df.rmse, cmap='viridis')
    plt.colorbar()

    plt.title("Prediction Error Distribution")
    plt.xlabel("y real")
    plt.ylabel("y predicted")

    plt.show()