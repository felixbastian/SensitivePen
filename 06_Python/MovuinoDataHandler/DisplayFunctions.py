import matplotlib.pyplot as plt

def Display(title, time, *args):

    nbGraph = len(args)
    for i in range(nbGraph):
        plt.subplot(nbGraph, 1, i+1)
        plt.plot(time, args[i][0], color = "red", label="x")
        plt.plot(time, args[i][1], color = "green", label="y")
        plt.plot(time, args[i][2], color = "blue", label="z")
        plt.legend()
    plt.title(title)
    plt.show()
