import numpy as np
import cv2 as cv
import os
import pandas as pd
import time
import traitementFichier as f

from scipy.spatial import distance
from sklearn.cluster import KMeans


# test sift
# img = cv.imread('./test.jpg')
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#
# sift = cv.xfeatures2d.SIFT_create()
# kp = sift.detect(gray,None)
#
# img = cv.drawKeypoints(gray,kp,img)
#
# cv.imwrite('sift_keypoints.jpg',img)

    # img = cv.imread('/home/utilisateur/Bureau/ChefOeuvre/data/VeRi_with_plate/image_train/'+nomsImage[])
    # cv.imshow('sample',img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()



def descripteurSift(cheminImage):
    img = cv.imread(cheminImage,cv.IMREAD_COLOR)
    sift = cv.xfeatures2d.SIFT_create()
    keypoints, descripteurs = sift.detectAndCompute(img,None)

    return descripteurs


def extraireDescripteursEntrainement(nomsImage,cheminImage,nbImg):

    #extraire les descripteurs de toutes les images
    dico = descripteurSift(cheminImage + "/" + nomsImage[0])
    print "descripteur 0 " + str(type(dico))
    for i in range(1,nbImg):
            descripteurs = descripteurSift(cheminImage + "/" + nomsImage[i])
            print type(descripteurs)
            dico = np.concatenate((dico,descripteurs))

    return dico

def calculerClassesDescripteurs(dicoDescripteur,k):
    dico = pd.DataFrame(dicoDescripteur)
    kmeans = KMeans(n_clusters=k).fit(dico)
    return kmeans

def calculerHistogrammeImage(cheminImage,kmeans,k):

        img = cv.imread(cheminImage,cv.IMREAD_COLOR)
        sift = cv.xfeatures2d.SIFT_create()
        keypoints, descripteurs = sift.detectAndCompute(img,None)

        histoG = np.zeros(k)
        nbKeypoints = np.size(keypoints)

        for des in descripteurs:
            ind = kmeans.predict([des])
            histoG[ind] += 1

        return histoG

def listerHistogrammeEntrainement(nomsImage,cheminImage,kmeans,k,nbImg):
    listeHistoG = []

    for i in range(0,nbImg):
        chemin = cheminImage + "/" + nomsImage[i]
        listeHistoG.append(calculerHistogrammeImage(chemin,kmeans,k))
    return listeHistoG

def calculerScoresSift(listeHistoG,histoGtest):
    scores = []
    for des in listeHistoG:
        scores.append(distance.euclidean(des,histoGtest))
    return scores

def testerFonctionsSift():
    cheminImage = '../data/VeRi_with_plate/image_train'
    cheminFichier = '../data/VeRi_with_plate/name_train.txt'
    cheminTest = '../data/VeRi_with_plate/image_test/0002_c002_00030600_0.jpg'
    nbImgTester = 5

    nomsImage = f.listerContenuFichier(cheminFichier)

    debut = time.time()
    dico = extraireDescripteursEntrainement(nomsImage,cheminImage,nbImgTester)
    fin = time.time()
    print "\tTemps de calcul du Dictionnaire de descripteurs Sift : " + str(fin-debut) + " secondes\n"
    print ("Taille du dictionnaire = " + str(np.size(dico)) + "\n")
    print ( "taille descripteurs" + str(np.size(dico,1)) + "\n")
    # print dico

    k = 1000
    debut = time.time()
    kmeans = calculerClassesDescripteurs(dico,k)
    fin = time.time()
    print "\tTemps de calcul des k centroides : " + str(fin-debut) + " secondes\n"

    debut = time.time()
    listeHistoG = listerHistogrammeEntrainement(nomsImage,cheminImage,kmeans,k,nbImgTester)
    fin = time.time()
    print "\tTemps de calcul des" + str(nbImgTester) + "descripteurs BOW-SIFT  : " + str(fin-debut) + " secondes\n"
    print "Nb histoG " + str(len(listeHistoG)) + " = Nombre d'image " + str(nbImgTester)
    print "Nb classe histoG = " + str(np.size(listeHistoG[0])) + " = k" + str(k)
    # print listeHistoG

    #Tester la reconnaissance image
    debut = time.time()
    histoGtest = calculerHistogrammeImage(cheminTest,kmeans,k)
    fin = time.time()
    print "\tTemps de calcul du descripteur BOW-SIFT de l'image test : " + str(fin-debut) + " secondes\n"

    debut = time.time()
    scores = calculerScoresSift(listeHistoG,histoGtest)
    fin = time.time()
    print "\tTemps de calcul des scores de distance euclidienne : " + str(fin-debut) + " secondes\n"
    # print scores
#main

testerFonctionsSift()




# print descripteurSift('test1.jpg')
