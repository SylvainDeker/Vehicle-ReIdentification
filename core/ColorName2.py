import sys
import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans
from ExtractColor2 import ExtractColor2

class ColorName2:
    """docstring for ColorName2."""

    def __init__(self,k=13):
        self.k = k
        self._ref_BGRcolor = np.zeros(self.k)

    def loadimgref(self,imagefullpath):
        exc = ExtractColor2(self.k)
        self._ref_BGRcolor = exc.getColorBGR(imagefullpath)

    def compareTo(self,imagefullpath):
        """Provide a score between 0 and 1, 1 = same color"""
        exc = ExtractColor2(self.k)
        bgrcolor = exc.getColorBGR(imagefullpath)

        score = 0
        for i in range(self.k):
            score += np.linalg.norm(bgrcolor[i] - self._ref_BGRcolor[i])/(np.sqrt(255*255*3))
        score /= self.k
        return 1 - score


if __name__ == '__main__':
    ref = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"

    # img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0009_c012_00068010_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0014_c016_00039135_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0006_c017_00023390_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0177_c016_00068270_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0042_c004_00087105_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0315_c019_00034675_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    img = "../data/VeRi_with_plate/image_query/0005_c002_00075750_0.jpg"
    cv.imwrite("testref.png",cv.imread(ref))
    cv.imwrite("testResColor.png",cv.imread(img))
    cn = ColorName2()
    cn.loadimgref(ref)
    score = cn.compareTo(img)
    print("score :" + str(score))

    # Smallest Score ever 0
    # c = [0,0,0]
    # cv.imwrite("Allblack.png",np.resize(c,(100,100,3)))
    # c = [255,255,255]
    # cv.imwrite("AllWhite.png",np.resize(c,(100,100,3)))
    #
    # cn.loadimgref("Allblack.png")
    # score = cn.compareTo("AllWhite.png")
    # print("score :" + str(score))
