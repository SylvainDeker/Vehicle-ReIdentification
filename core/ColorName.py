import sys
import numpy as np
from ImageVehicle import ImageVehicle
import cv2 as cv
from sklearn.cluster import KMeans

class ColorName:
    """docstring for ImageVehicle."""

    def __init__(self):
        self.kmeans = None
        self.k = 0


    def extract_patchs(self,image_vehicule:ImageVehicle):
        desc = np.empty((16,3))
        # img2 = image_vehicule.image
        # cv.imwrite("test.png",img2)
        img2 = image_vehicule.image[0:16:4,4:32:8]
        # cv.imwrite("test2.png",img2)
        desc = np.reshape(img2,(16,3))
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




if __name__ == '__main__':
    # img = cv.imread("../data/VeRi_with_plate/image_query/0006_c015_00022375_0.jpg")
    # img = cv.imread("../data/VeRi_with_plate/image_query/0300_c013_00078770_0.jpg")
    # img = cv.imread("../data/VeRi_with_plate/image_query/0002_c002_00030600_0.jpg")
    # img = cv.imread("../data/VeRi_with_plate/image_query/0063_c016_00007580_0.jpg")
    img = cv.imread("../data/VeRi_with_plate/image_query/0172_c011_00078830_0.jpg")


    img = cv.resize(img,(32,16))
    cv.imwrite("test_ref.png",img)
    iv = ImageVehicle(img,"/chemin/video",((0,0,0,0,0,0)),42)
    cn = ColorName()
    desc = cn.extract_patchs(iv)
    cv.imwrite("test_desc.png",np.resize(desc,(16,1,3)))

    # print(desc)
    print("----------KMMEANS Test-----------")
    # Example of clusters
    rouge = [255,0,0]
    jaune = [255,255,0]
    jaune2 = [255,255,10]
    vert = [0,255,0]
    bleu = [0,0,255]
    white = [255,255,255]
    X = np.array([rouge,vert,jaune2,bleu,jaune,white])

    cn.fitKMeans(X,4)
    Xres,label_dominant = cn.bow_process(desc)
    cv.imwrite("test_Xres.png",np.resize(Xres,(len(Xres),1,3)))
    result_color = cn.resultColor(Xres)
    cv.imwrite("test_ResColor.png",np.resize(result_color,(1,1,3)))

    score = cn.score(result_color,label_dominant)
    print("Score")
    print(score)
