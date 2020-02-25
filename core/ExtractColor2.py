import sys
import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans
import pickle


class ExtractColor2:
    """docstring for ExtractColor2."""

    def __init__(self,k=10):
        self.k = k

    def load(self,imagefullpath):
        img = cv.imread(imagefullpath)


        # kernel = np.matrix([[0,1,0],[1,1,1],[0,1,0]],np.uint8)
        #
        # img = cv.erode(img,kernel,iterations = 1)
        return img

    def extract_patchs(self,img):
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




        lenPatch = img.shape[0]*img.shape[1]
        desc = np.empty((lenPatch,3))
        desc = np.reshape(img,(lenPatch,3))
        descbgr = desc

        # Labimg = cv.cvtColor(np.resize(img,(lenPatch,1,3)), cv.COLOR_BGR2LAB)
        # Lab = np.reshape(Labimg,(-1,3))
        # desc = Lab



        if len(desc)==0:
            print("ERROR: Empty descriptor")
        return desc,descbgr


    def bow_process(self,desc,descbgr,k):

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
        Xres = np.zeros((k,3))
        div = np.zeros((k,3))
        ctr = 0

        for i in range(len(desc)):
            Xres[res[i]] += descbgr[i]
            div[res[i]] += 1
        Xres = Xres / div
        Xres = np.int32(Xres)


        res1 = np.concatenate((Xres,np.reshape(hist,(len(Xres),1))),axis=1)

        # print(res1)
        dtype=[]
        res2 = np.sort(res1,axis=1)
        # print(res2)

        dtype = [('Blue',int),('Green',int),('Red',int),('Hist',int)]
        value = []
        for i in range(k):
            value.append((Xres[i][0],Xres[i][1],Xres[i][2],hist[i]))

        new_value = np.array(value,dtype=dtype)

        # print(new_value)

        new_value = np.sort(new_value,order=['Hist'])

        # print(new_value)

        result = np.empty((self.k,3))
        # print(result)
        for i in range(k):
            result[i][0] = new_value[i][0]
            result[i][1] = new_value[i][1]
            result[i][2] = new_value[i][2]

        return result

    def getColorBGR(self,imagefullpath):
        img = self.load(imagefullpath)
        desc,descbgr = self.extract_patchs(img)
        result = self.bow_process(desc,descbgr,self.k)



        return result

    # def getColorRGB(self,imagefullpath):
    #     bgr = self.getColorBGR(imagefullpath)
    #     rgb = [bgr[2],bgr[1],bgr[0]]
    #     return rgb


if __name__ == '__main__':
    img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0122_c001_00036500_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"

    cv.imwrite("testref.png",cv.imread(img))
    ec = ExtractColor2()
    res = ec.getColorBGR(img)
    # res = ec.getColorRGB(img)
    cv.imwrite("testdesc.png",np.resize(res,(ec.k,1,3)))
    print(res)
