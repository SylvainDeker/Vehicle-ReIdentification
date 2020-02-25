import cv2 as cv
import numpy as np
import csv
import sys
import os
import time
from ExtractColor import ExtractColor

def _disparity(image):
    img = np.int32(cv.imread(image))
    center = np.mean(np.mean(img,axis=0),axis=0)
    lenPatch = img.shape[0]*img.shape[1]

    a = np.reshape(img,(lenPatch,3))
    value = np.sum(np.linalg.norm( a - center,axis=1))
    return value
def disparity(k,lim):
    os.system("python3 ExtractColorTest.py "+ str(k)+ " "+ str(lim))
    acc = [0,0,0,0,0,0,0]
    acc[0] = _disparity("./imgtest/white.png")
    acc[1] = _disparity("./imgtest/green.png")
    acc[2] = _disparity("./imgtest/marineblue.png")
    acc[3] = _disparity("./imgtest/orange.png")
    acc[4] = _disparity("./imgtest/red.png")
    acc[5] = _disparity("./imgtest/black.png")
    acc[6] = _disparity("./imgtest/yellow.png")
    # print(np.int32(acc))
    return np.int32(np.sum(acc))


def manual(fichierCSV,k,lim):
    with open(fichierCSV) as csvfile:
        cr = csv.reader(csvfile,delimiter=',',quotechar='"')
        err = 0
        ctr=0
        for row in cr:
            path = row[0]
            rgb_ref = [int(row[1]),int(row[2]),int(row[3])]
            exc = ExtractColor(k,lim)
            regb_test = exc.getColorRGB(path)
            err += np.linalg.norm(np.array(rgb_ref)-np.array(regb_test))
            ctr+=1
        return err/(ctr*np.sqrt(255*255*3))

if __name__ == '__main__':

    k = int(sys.argv[1])
    lim = int(sys.argv[2])

    d = disparity(k,lim)
    m1 = manual("test1.csv",k,lim)
    m2 = manual("test2.csv",k,lim)
    print(str(k)+","+str(lim)+","+str(d)+","+str(m1)+","+str(m2))

    # stime = time.time()
    # k = 8
    # lim = 1
    # d = disparity(k,lim)
    # m1 = manual("test1.csv",k,lim)
    # m2 = manual("test2.csv",k,lim)
    # print(str(k)+","+str(lim)+","+str(d)+","+str(m1)+","+str(m2))
    # print("%s secondes " % (time.time() - stime) )
