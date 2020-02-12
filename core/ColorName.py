import sys
import numpy as np
from ImageVehicle import ImageVehicle
from buildSetImageVehicle import buildSetImageVehicle
from displayPLot import displayPLot
from histoPLot import histoPLot
import cv2 as cv
from sklearn.cluster import KMeans

class ColorName:
    """docstring for ImageVehicle."""

    def __init__(self):
        self.kmeans = None
        self.k = 0

    def preprocessing(self,image_vehicule:ImageVehicle):
        img = cv.imread(image_vehicule.image)
        if img.shape[0]>img.shape[1]:
            min = img.shape[1]
        else:
            min = img.shape[1]

        edge = np.int32(0.2*min)
        coef = 4
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



    def fitKMeans(self,X,k):

        self.k = k
        self.kmeans = KMeans(n_clusters=self.k,random_state=0)
        self.kmeans.fit(X)



    def bow_process(self,desc):
        # print("Labels:")
        # print(kmeans.labels_)
        # print("Cluster Centers:")
        # print(kmeans.cluster_centers_)
        # print("Predict:")
        # # desc = np.ones((16,3))*[255,255,0]
        # # print(desc)
        res = self.kmeans.predict(desc)
        # print(res)
        # print("Histo:")
        hist,_ = np.histogram(res,bins=range(self.k+1))
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

    def score(self,result_color,label_dominant):
        # print("mmmm")
        # print(moyenne)
        # cv.imwrite("test4.png",np.resize(Xres,(1,1,3)))
        return np.linalg.norm(result_color-self.kmeans.cluster_centers_[label_dominant])

    def resultColor(self,Xres):
        moyenne = np.mean(Xres,axis=0)
        return moyenne

    def trainColorName(self,ArrayOfImageVehicle):
        NbImages = len(ArrayOfImageVehicle)
        colors = np.empty((NbImages,3))
        for i in range(NbImages):
            img = cn.preprocessing(ArrayOfImageVehicle[i])
            desc = self.extract_patchs(img)
            self.fitKMeans(desc,10)
            Xres,label_dominant = cn.bow_process(desc)
            # cv.imwrite("test_Xres.png",np.resize(Xres,(len(Xres),1,3)))
            colors[i] = cn.resultColor(Xres)
            print(i)
        return colors




if __name__ == '__main__':
    # img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"
    #
    #
    iv = ImageVehicle(img,"/chemin/video",((0,0,0,0,0,0)),42)
    cn = ColorName()
    img = cn.preprocessing(iv)
    cv.imwrite("test_ref.png",img)
    desc = cn.extract_patchs(img)
    cv.imwrite("test_desc.png",np.resize(desc,(desc.shape[0],1,3)))

    # print(desc)
    print("----------KMMEANS Test-----------")
    # Example of clusters
    # rouge = [255,0,0]
    # jaune = [255,255,0]
    # vert = [0,255,0]
    # bleu = [0,0,255]
    #
    # white = [255,255,255]
    # gray = [128,128,128]
    # black = [0,0,0]
    # X = np.array([rouge,jaune,vert,bleu,gray,white,black])

    cn.fitKMeans(desc,5)
    Xres,label_dominant = cn.bow_process(desc)
    cv.imwrite("test_Xres.png",np.resize(Xres,(len(Xres),1,3)))
    result_color = cn.resultColor(Xres)
    print(result_color)
    cv.imwrite("test_ResColor.png",np.resize(result_color,(1,1,3)))

    score = cn.score(result_color,label_dominant)
    displayPLot(desc[0:len(desc):1])
    displayPLot(Xres[0:len(Xres):1])
    print("Score")
    print(score)

    # print("--------trainColor--------------")
    # x=10
    # y=10
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/white/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("white.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/green/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("green.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/marineblue/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("marineblue.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/orange/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("orange.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/red/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("red.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/black/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("black.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorName()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/yellow/",x*y)
    # colors = cn.trainColorName(arrayOfImageVehicle)
    # cv.imwrite("yellow.png",np.resize(colors,(x,y,3)))











    # np.savetxt('colors.csv', colors, fmt='%i')
