import matplotlib.pyplot as plt

def DisplayChartsV3(title, time, shape, *args):
    """
    Display mutlitple charts
    :param title:
    :param time:
    :param args: charts ton plot, must be list with 3 list of you vector components
    :return:
    """
    nbGraph = len(args)
    for i in range(nbGraph):
        plt.subplot(shape * 10 + i+1)
        plt.plot(time, args[i][0], color = "red", label="x")
        plt.plot(time, args[i][1], color = "green", label="y")
        plt.plot(time, args[i][2], color = "blue", label="z")
        plt.legend()
    plt.title(title)
    plt.show()

def PlotVector(t, v, title, pos):
    """
    Plot numpy vector, must have 3 components

    v = np.array(np.array(vxi vyi vzi))
    :param t:
    :param v: List of Vector numpy
    :param title:
    :param pos:
    :return:
    """
    fig = plt.subplot(pos)
    fig.plot(t, v[:, 0], color="r", label="x")
    fig.plot(t, v[:, 1], color="green", label ='y')
    fig.plot(t, v[:, 2], color="blue", label = 'z')
    fig.set_title(title)

    return fig


def plotVect(t, v, title, pos):
    """
    Plot vector list

    v = [ vx vy vz]  with vx, vy, vz lists of vectors
    :param t:
    :param vx:
    :param vy:
    :param vz:
    :param title:
    :param pos: must be list with 3 list of you vector components
    :return:
    """
    fig = plt.subplot(pos)
    fig.plot(t, v[0], color="r")
    fig.plot(t, v[1], color="green")
    fig.plot(t, v[2], color="blue")
    fig.set_title(title)
