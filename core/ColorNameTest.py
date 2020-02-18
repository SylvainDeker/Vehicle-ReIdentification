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

class ColorNameTest:
    """docstring for ImageVehicle."""

    def __init__(self):
        self.kmeans = None
        self.k = 0

    def preprocessing(self,image_vehicule:ImageVehicle):
        img = cv.imread(image_vehicule.image)
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

    def extractColorsFromImages(self,ArrayOfImageVehicle):
        NbImages = len(ArrayOfImageVehicle)
        colors = np.empty((NbImages,3))
        for i in range(NbImages):
            img = cn.preprocessing(ArrayOfImageVehicle[i])
            desc = self.extract_patchs(img)
            # self.fitKMeansTest(desc,8)
            Xres,label_dominant = cn.bow_process(desc,8)
            # cv.imwrite("test_Xres.png",np.resize(Xres,(len(Xres),1,3)))
            colors[i] = cn.resultColor(Xres)
            print(i)
        return colors

    def fitKMEANS(self,k,colors):
        self.k = k
        self.kmeans = KMeans(n_clusters=self.k,random_state=0)
        self.kmeans.fit(colors)


    def getClusters(self):
        return self.kmeans.cluster_centers_

    def getCentroids(self):
        colors_res = np.zeros((self.k,3))

        div = np.zeros((self.k,1))+1
        for i in range(len(colors)):
            div[res[i]] = div[res[i]]+1;
            colors_res[res[i]] = colors_res[res[i]] + colors[i]

        return colors_res/div

    def saveKMeans(self,filename):
        pickle.dump(self.kmeans, open(filename, 'wb'))

    def loadKMeans(self,filename):
        self.kmeans = pickle.load(open(filename, 'rb'))
        return self.kmeans

    def init(self):
        # self.loadKMeans("10.kmns")
        yellow = [25,100,100]
        orange = [42,57,106]

        green =  [0  ,255,0  ]
        gray =   [128,128,128]
        red =    [0  ,0  ,255]
        blue =   [255,0  ,0  ]
        white =  [255,255,255]
        golden = [32 ,165,218]
        brown =  [42 ,42 ,165]
        black =  [0  ,0  ,0  ]


        weight = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        # weight = [1,0,0,0,0,0,0,0,0,0]
        X=np.array([yellow,orange,green,gray ,red,blue,white,golden,brown,black])
        # displayPLot(X)
        lab = [1,2,3,4,5,6,7,8,9,10]
        self.kmeans = KMeans(n_clusters=9,random_state=0)
        self.kmeans.fit(X,sample_weight=weight)


    def predict(self,imageVehicle):
        img = self.preprocessing(imageVehicle)
        desc = self.extract_patchs(img)
        Xres,label_dominant = cn.bow_process(desc,k=8)
        result_color = cn.resultColor(Xres)
        # print("ref:")
        # print(result_color)
        label = self.kmeans.predict(np.resize(result_color,(1,3)))
        score = np.linalg.norm(result_color - self.kmeans.cluster_centers_[label][0])
        return self.kmeans.cluster_centers_[label][0],score



if __name__ == '__main__':
    # img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"
    #
    #
    # iv = ImageVehicle(img,"/chemin/video",((0,0,0,0,0,0)),42)
    # img = cv.imread(img)
    # cn = ColorNameTest()
    # img = cn.preprocessing(iv)
    # cv.imwrite("test_ref.png",img)
    # desc = cn.extract_patchs(img)
    # cv.imwrite("test_desc.png",np.resize(desc,(desc.shape[0],1,3)))
    #
    # # print(desc)
    # print("----------KMMEANS Test-----------")
    # # Example of clusters
    # rouge = [255,0,0]
    # jaune = [255,255,0]
    # vert = [0,255,0]
    # bleu = [0,0,255]
    #
    # white = [255,255,255]
    # gray = [128,128,128]
    # black = [0,0,0]
    # X = np.array([rouge,jaune,vert,bleu,gray,white,black])
    #
    #
    # Xres,label_dominant = cn.bow_process(desc,5)
    # cv.imwrite("test_Xres.png",np.resize(Xres,(len(Xres),1,3)))
    # result_color = cn.resultColor(Xres)
    # print(result_color)
    # cv.imwrite("test_ResColor.png",np.resize(result_color,(1,1,3)))
    #
    # displayPLot(desc[0:len(desc):1])
    # displayPLot(Xres[0:len(Xres):1])


    # print("--------trainColor--------------")
    # x=6
    # y=6
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/white/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("white.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/green/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("green.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/marineblue/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("marineblue.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/orange/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("orange.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/red/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("red.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/black/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("black.png",np.resize(colors,(x,y,3)))
    #
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/testperso/yellow/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # print(np.linalg.norm(colors - (74,145,63))/(x*y))
    # cv.imwrite("yellow.png",np.resize(colors,(x,y,3)))


    # x = 300
    # y = 100
    # cn = ColorNameTest()
    # arrayOfImageVehicle = buildSetImageVehicle("../data/VeRi_with_plate/image_test/",x*y)
    # colors = cn.extractColorsFromImages(arrayOfImageVehicle)
    # np.savetxt('colors.csv', colors, fmt='%i')
    # cv.imwrite("colors.png",np.resize(colors,(x,y,3)))



    # cn = ColorNameTest()
    # colors = np.loadtxt("colors.csv")
    # cn.fitKMEANS(10,colors)
    # res = cn.getClusters()
    # print(res)
    # cn.saveKMeans("10.kmns")
    # cv.imwrite("colors.png",np.resize(res,(10,1,3)))

    # cn = ColorNameTest()
    # cn.loadKMeans("100.kmns")
    # # res = cn.fitKMEANS(400,colors)
    # res = cn.getClusters()
    # cv.imwrite("colors.png",np.resize(res,(16,25,3)))
    #
    # print(np.int32(res))

    img = "../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg"
    # img = "../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg"

    img2 = cv.imread(img)
    cv.imwrite("test_ref.png",img2)
    cn = ColorNameTest()
    cn.init()
    iv = ImageVehicle(img,"/chemin/video",((0,0,0,0,0,0)),42)
    res,score = cn.predict(iv)
    print("drep:")
    print(res)
    print(score/255)
    cv.imwrite("test_ResColor.png",np.resize(res,(1,1,3)))
