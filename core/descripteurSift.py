import numpy as np
import cv2 as cv
import os
import pandas as pd
import time
import pickle
import gc
import traitementFichier as f

from scipy.spatial import distance
from sklearn.cluster import MiniBatchKMeans


def descripteurSift(cheminImage):
    img = cv.imread(cheminImage,cv.IMREAD_COLOR)
    sift = cv.xfeatures2d.SIFT_create()
    keypoints, descripteurs = sift.detectAndCompute(img,None)

    return descripteurs


def extraireDescripteursEntrainement(nomsImage,cheminImage,nbImg):

    #extraire les descripteurs de toutes les images
    print nomsImage[0]
    dico = descripteurSift(cheminImage + "/" + nomsImage[0])
    for i in range(1,nbImg):
            print nomsImage[i]
            descripteurs = descripteurSift(cheminImage + "/" + nomsImage[i])
            print type(descripteurs)
            dico = np.concatenate((dico,descripteurs))
            print descripteurs.shape
    return dico

def creerFichiersDico(nomsImage,cheminImage,cheminRepDes,indDIm,indFIm):
    for i in range(indDIm,indFIm):
        descripteurs = descripteurSift(cheminImage + "/" + nomsImage[i])
        nbDes,tailleDes = descripteurs.shape
        f.ecrireFichierDes(descripteurs,nomsImage[i],cheminRepDes,"/desSift_")


def extraireDico(cheminRepDes,nomsFichierDes,indDIm,indFIm,pas):
    dico = f.extraireDescripteursFichier(cheminRepDes + "/" + nomsFichierDes[indDIm])
    # print "Dico = " + str(dico.shape
    for i in range(indDIm,indFIm,pas):
        descripteurs = f.extraireDescripteursFichier(cheminRepDes + "/" + nomsFichierDes[i])
        dico = np.concatenate((dico,descripteurs))
    return dico


def calculerClassesDescripteurs(dicoDescripteur,k,bs):
    dico = pd.DataFrame(dicoDescripteur)
    kmeans = MiniBatchKMeans(n_clusters=k,batch_size=bs,verbose=1).fit(dico)
    print kmeans

    pickle.dump(kmeans,open("../data/ressources/modeleBOWSIFT.pkl","wb"))


def calculerHistogrammeImage(cheminImage,kmeans,k):
    kmeans.verbose = False

    img = cv.imread(cheminImage,cv.IMREAD_COLOR)
    sift = cv.xfeatures2d.SIFT_create()
    keypoints, descripteurs = sift.detectAndCompute(img,None)

    histoG = np.zeros((1,k))
    nbKeypoints = np.size(keypoints)

    for des in descripteurs:
        ind = kmeans.predict([des])
        histoG[0][ind] += 1

    nbKeyPoints = np.size(keypoints)
    # histoG = histoG / nbKeypoints

    return histoG

def calculerHistogrammeEntrainement(nomsImage,cheminImage,cheminRepDesBOWSIFT,kmeans,k,nbImg):
    for i in range(0,nbImg):
        chemin = cheminImage + "/" + nomsImage[i]
        descripteurBOWSIFT = calculerHistogrammeImage(chemin,kmeans,k)
        f.ecrireFichierDes(descripteurBOWSIFT,nomsImage[i],cheminRepDesBOWSIFT,"/desBOWSift_")


def listerDesBOWSIFT(cheminRepDesBOWSIFT,nomsFichierBOWSIFT,indDIm,indFIm,pas):
    desBOWSIFT = []
    for i in range(indDIm,indFIm,pas):
        descripteur = f.extraireDescripteursFichier(cheminRepDesBOWSIFT + "/" + nomsFichierBOWSIFT[i])
        desBOWSIFT.append(descripteur)

    return desBOWSIFT

def recupererDesBOWSIFT(nomImage):
    nomImage = nomImage.strip(".jpg")
    des = f.extraireDescripteursFichier('../data/ressources/descripteursBOWSift/desBOWSift_' + nomImage + '.txt')
    return des

def calculerScoresSift(listeHistoG,histoGtest):
    scores = []
    for des in listeHistoG:
        scores.append(distance.euclidean(des,histoGtest))
    return scores
