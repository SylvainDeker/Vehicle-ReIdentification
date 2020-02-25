from ExtractColor import ExtractColor
import os
import sys
import numpy as np
import cv2 as cv

def indexJPG(pathfolder,limitNumber=100000):
    # if limitNumber==0 -> no limite, all the images in the folder are loaded.
    files = os.listdir(pathfolder)
    n = len(files)
    # print(n)
    ArrayOfImageVehicle = []
    i=0
    for name in files:
        if ".jpg".lower() in name.lower():
            ArrayOfImageVehicle.append(pathfolder+name)
            i = i+1
            if i==limitNumber:
                return ArrayOfImageVehicle
    return ArrayOfImageVehicle

def extractColorsFromImages(ArrayOfImageVehicle,k,lim):
    exc = ExtractColor(k,lim)
    NbImages = len(ArrayOfImageVehicle)
    colors = np.empty((NbImages,3))
    for i in range(NbImages):
        bgr = exc.getColorBGR(ArrayOfImageVehicle[i])
        colors[i] = bgr
    return colors

def test1(k,lim):
    x=10
    y=10

    index = indexJPG("../data/VeRi_with_plate/testperso/white/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/white.png",np.resize(colors,(x,y,3)))

    index = indexJPG("../data/VeRi_with_plate/testperso/green/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/green.png",np.resize(colors,(x,y,3)))

    index = indexJPG("../data/VeRi_with_plate/testperso/marineblue/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/marineblue.png",np.resize(colors,(x,y,3)))


    index = indexJPG("../data/VeRi_with_plate/testperso/orange/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/orange.png",np.resize(colors,(x,y,3)))

    index = indexJPG("../data/VeRi_with_plate/testperso/red/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/red.png",np.resize(colors,(x,y,3)))

    index = indexJPG("../data/VeRi_with_plate/testperso/black/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/black.png",np.resize(colors,(x,y,3)))

    index = indexJPG("../data/VeRi_with_plate/testperso/yellow/",x*y)
    colors = extractColorsFromImages(index,k,lim)
    cv.imwrite("imgtest/yellow.png",np.resize(colors,(x,y,3)))

if __name__ == '__main__':
    test1(int(sys.argv[1]),int(sys.argv[2]))
