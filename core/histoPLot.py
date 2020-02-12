import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def histoPLot(X,label,k):
    print(X)
    print(label)
    print(k)
    hist,_ = np.histogram(X,bins=range(k+1))
    colors = np.zeros((k,3))
    print(colors)
    colors = np.array([[1,0.5,0],
                        [0,1,0],
                        [0,1,0],
                        [0,1,0],
                        [0,0,1],
                        [1,0,0]])

    y = hist
    plot = plt.scatter(y, y, c = colors)
    plt.clf()
    plt.bar(range(len(y)), y, color = colors)
    plt.show()


if __name__ == '__main__':
    histoPLot()
