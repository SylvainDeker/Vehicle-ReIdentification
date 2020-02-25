import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import csv
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
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)
    ax.scatter(reds, greens, blues, marker='o',c=colo)


    # Reference
    # rouge = [255,0,0]
    # jaune = [255,255,0]
    # vert = [0,255,0]
    # bleu = [0,0,255]
    # jsp = [0,255,255]
    # white = [255,255,255]
    # jsp2 = [255,0,255]
    # black = [0,0,0]
    # ref = np.array([rouge,jaune,vert,bleu,jsp,jsp2,white,black])
    # colo = ref/255
    # ax.scatter(ref[:,0] ,ref[:,1], ref[:,2], marker='s',c=colo)

    ax.set_xlabel('RED')
    ax.set_ylabel('GREEN')
    ax.set_zlabel('BLUE')

    plt.show()



def displayPLotRGB(X:np.ndarray):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    reds = np.array(X[:,0])
    greens = np.array(X[:,1])
    blues = np.array(X[:,2])
    # rgb = np.concatenate((reds,greens,blues),axis=0)
    # rgb = rgb.reshape((X.shape[0],3))

    colo = np.array([reds,greens,blues]).T
    colo = colo/255
    ax.scatter(reds, greens, blues, marker='o',c=colo)
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)

    # Reference
    # rouge = [255,0,0]
    # jaune = [255,255,0]
    # vert = [0,255,0]
    # bleu = [0,0,255]
    # jsp = [0,255,255]
    # white = [255,255,255]
    # jsp2 = [255,0,255]
    # black = [0,0,0]
    # ref = np.array([rouge,jaune,vert,bleu,jsp,jsp2,white,black])
    # colo = ref/255
    # ax.scatter(ref[:,0] ,ref[:,1], ref[:,2], marker='s',c=colo)

    ax.set_xlabel('X Label = RED')
    ax.set_ylabel('Y Label = GREEN')
    ax.set_zlabel('Z Label = BLUE')

    plt.show()


def displayPLotBGRinLAB(X:np.ndarray):


    Labimg = cv.cvtColor(np.resize(X,(len(X),1,3)), cv.COLOR_BGR2LAB)
    Lab = np.reshape(Labimg,(-1,3))

    print(Lab)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)
    L = Lab[:,0]
    a = Lab[:,1]
    b = Lab[:,2]

    reds = np.array(X[:,2])
    greens = np.array(X[:,1])
    blues = np.array(X[:,0])
    # rgb = np.concatenate((reds,greens,blues),axis=0)
    # rgb = rgb.reshape((X.shape[0],3))

    colo = np.array([reds,greens,blues]).T
    colo = colo/255
    ax.scatter(L, a, b, marker='o',c=colo)


    ax.set_xlabel('L')
    ax.set_ylabel('a')
    ax.set_zlabel('b')

    plt.show()

def basic3DPlot(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X, Y, Z, marker='o',c='red')
    ax.bar3d(X, Y, 0.15, 0.01, 0.1, np.array(Z)-0.15, shade=True)


    ax.set_xlabel('K')
    ax.set_ylabel('Lim')
    ax.set_zlabel('Result')

    plt.show()

def ResultMethod(fichierCSV):
    with open(fichierCSV) as csvfile:
        cr = csv.reader(csvfile,delimiter=',',quotechar='"')
        # err = 0
        # ctr=0
        x = []
        y = []
        res = []
        for row in cr:
            x.append(int(row[0]))
            y.append(int(row[1]))
            res.append(float(row[3]))
            # err += np.linalg.norm(np.array(rgb_ref)-np.array(regb_test))

        # return err/(ctr*np.sqrt(255*255*3))

        print(x)
        print(y)
        print(res)

        #
        # x = np.int32(np.array(x))
        # y = np.int32(np.array(y))
        # res = np.float32(np.array(res))

        basic3DPlot(x,y,res)

if __name__ == '__main__':
    # img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"
    # img = "test.png"
    # img = cv.imread(img)
    # cv.imwrite("test.png",img)
    #
    # data = np.reshape(img,(img.shape[0]*img.shape[1],3));
    # displayPLotBGRinLAB(data[0:len(data)])

    ResultMethod("ResultLbaMethod.csv")
