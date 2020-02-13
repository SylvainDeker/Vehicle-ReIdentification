import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import



def displayPLot(X:np.ndarray):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    reds = np.array(X[:,2])
    greens = np.array(X[:,1])
    blues = np.array(X[:,0])
    # rgb = np.concatenate((reds,greens,blues),axis=0)
    # rgb = rgb.reshape((X.shape[0],3))

    colo = np.array([reds,greens,blues]).T
    colo = colo/255
    ax.scatter(reds, greens, blues, marker='o',c=colo)


    # Reference
    rouge = [255,0,0]
    jaune = [255,255,0]
    vert = [0,255,0]
    bleu = [0,0,255]
    jsp = [0,255,255]
    white = [255,255,255]
    jsp2 = [255,0,255]
    black = [0,0,0]
    ref = np.array([rouge,jaune,vert,bleu,jsp,jsp2,white,black])
    colo = ref/255
    ax.scatter(ref[:,0] ,ref[:,1], ref[:,2], marker='s',c=colo)

    ax.set_xlabel('X Label = RED')
    ax.set_ylabel('Y Label = GREEN')
    ax.set_zlabel('Z Label = BLUE')

    plt.show()


if __name__ == '__main__':
    # img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"

    # img = cv.imread(img)
    # data = np.reshape(img,(img.shape[0]*img.shape[1],3));
    # displayPLot(data)

    loaded = np.loadtxt("colors.csv")
    displayPLot(loaded)
    print(loaded)
