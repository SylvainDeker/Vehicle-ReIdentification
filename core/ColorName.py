import sys
import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans
from ExtractColor import ExtractColor

class ColorName:
    """docstring for ColorName."""

    def __init__(self):
        self._ref_RGBcolor = [-1,0,0]

    def loadimgref(self,imagefullpath):
        exc = ExtractColor()
        self._ref_RGBcolor = exc.getColorRGB(imagefullpath)

    def compareTo(self,imagefullpath):
        """Provide a score between 0 and 1, 1 = same color"""
        exc = ExtractColor()
        rgbcolor = exc.getColorRGB(imagefullpath)
        return 1 - np.linalg.norm(np.array(rgbcolor) - np.array(self._ref_RGBcolor))/(np.sqrt(255*255*3))


if __name__ == '__main__':
    ref = "../data/VeRi_with_plate/image_query/0005_c004_00077625_0.jpg"
    img = "../data/VeRi_with_plate/image_query/0005_c003_00077670_0.jpg"

    cn = ColorName()
    cn.loadimgref(ref)
    score = cn.compareTo(img)
    print("score :" + str(score))

    # Smallest Score ever 0
    c = [0,0,0]
    cv.imwrite("Allblack.png",np.resize(c,(100,100,3)))
    c = [255,255,255]
    cv.imwrite("AllWhite.png",np.resize(c,(100,100,3)))

    cn.loadimgref("Allblack.png")
    score = cn.compareTo("AllWhite.png")
    print("score :" + str(score))
