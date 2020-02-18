import sys
import numpy as np
from ImageVehicle import ImageVehicle
from buildSetImageVehicle import buildSetImageVehicle
from displayPLot import displayPLot
from displayPLot import displayPLotRGB
from histoPLot import histoPLot
import cv2 as cv
from sklearn.cluster import KMeans
import pickle


class ExtractColor:
    """docstring for ExtractColor."""

    # def __init__(self):

    def load(self,imagefullpath):
        img = cv.imread(imagefullpath)

        if img.size ==0:
            print("Error reading img")
        if img.shape[0]>img.shape[1]:
            min = img.shape[1]
        else:
            min = img.shape[0]

        edge = np.int32(0.2*min)
        coef = 3
        img = cv.blur(img, (coef+1,coef+1))
        img = img[edge:img.shape[0]-edge:coef,edge:img.shape[1]-edge:coef]
        # kernel = np.matrix([[0,1,0],[1,1,1],[0,1,0]],np.uint8)
        #
        # img = cv.erode(img,kernel,iterations = 1)
        return img

    def extract_patchs(self,img):
        lenPatch = img.shape[0]*img.shape[1]
        desc = np.empty((lenPatch,3))
        desc = np.reshape(img,(lenPatch,3))
        if len(desc)==0:
            print("ERROR: Empty descriptor")
        return desc


    def bow_process(self,desc,k):

        kmeans = KMeans(n_clusters=k,random_state=0)
        kmeans.fit(desc)
        # print("Labels:")
        # print(kmeans.labels_)
        # print("Cluster Centers:")
        # print(kmeans.cluster_centers_)
        # print("Predict:")
        # # desc = np.ones((16,3))*[255,255,0]
        # # print(desc)
        res = kmeans.predict(desc)
        # print(res)
        # print("Histo:")
        hist,_ = np.histogram(res,bins=range(k+1))
        # print(hist)
        # print("Label dominant:")
        label_dominant = np.argmax(hist)
        # print(label_dominant)
        # print("Couleur pertinante")
        # print(kmeans.cluster_centers_[label_dominant])
        Xres = np.empty((hist[label_dominant],3))
        ctr = 0

        for i in range(len(desc)):
            if res[i]==label_dominant:
                Xres[ctr] = desc[i]
                ctr+=1

        # cv.imwrite("test3.png",np.resize(Xres,(16,1,3)))
        return Xres,label_dominant

    def resultColor(self,Xres):
        moyenne = np.mean(Xres,axis=0)
        return moyenne

    def getColorBGR(self,imagefullpath):
        img = self.load(imagefullpath)
        desc = self.extract_patchs(img)
        Xres,_ = self.bow_process(desc,8)
        bgr = self.resultColor(Xres)
        return bgr

    def getColorRGB(self,imagefullpath):
        bgr = self.getColorBGR(imagefullpath)
        rgb = [bgr[2],bgr[1],bgr[0]]
        return rgb

if __name__ == '__main__':
    img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    ec = ExtractColor()
    res = ec.getColorBGR(img)
    cv.imwrite("test_ResColor.png",np.resize(res,(1,1,3)))
    res = ec.getColorRGB(img)
    print(res)

    
