import os
import numpy as np
import cv2 as cv
from ImageVehicle import ImageVehicle

def buildSetImageVehicle(pathfolder,limitNumber=100000):
    # if limitNumber==0 -> no limite, all the images in the folder are loaded.
    files = os.listdir(pathfolder)
    n = len(files)
    # print(n)
    ArrayOfImageVehicle = []
    i=0
    for name in files:
        if ".jpg".lower() in name.lower():
            # print(name)
            # img = cv.imread(pathfolder + name)
            # TODO: MetaDATA
            ArrayOfImageVehicle.append(ImageVehicle(pathfolder+name,"",(0,0,0,0,0,0),i))
            i = i+1
            if i==limitNumber:
                return ArrayOfImageVehicle
    return ArrayOfImageVehicle

if __name__ == '__main__':
    list = buildSetImageVehicle("../data/VeRi_with_plate/image_test/",10)

    iv = list[9]
    print(type(iv.image))
    im = cv.imread(iv.image)
    cv.imwrite("test.png",im)
