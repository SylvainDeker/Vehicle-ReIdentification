import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


if __name__ == '__main__':
    img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"

    img = cv.imread(img)
    cv.imwrite("testref.png",img)
    imgHLS = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    # print(type(imgHLS[0][0][0]))
    imgHLS = np.uint8(imgHLS*[1,0,0]+[0,100,100])
    # print(type(imgHLS[0][0][0]))
    img = cv.cvtColor(imgHLS, cv.COLOR_HLS2BGR)
    cv.imwrite("test.png",img)


    # color = ('r','g','b')
    # for i,col in enumerate(color):
    #     histr = cv.calcHist([imgHLS],[i],None,[256],[0,256])
    #
    #     # histr.colorbar(images[0], ax=axs, orientation='horizontal', fraction=.1)
    #     plt.plot(histr)
    #     # plt.xlim([0,256])
    # plt.show()
