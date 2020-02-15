import numpy as np
import cv2 as cv
import os
import pandas as pd
import time
import pickle
import traitementFichier as f

from scipy.spatial import distance
from sklearn.cluster import KMeans


def descripteurSift(cheminImage):
    img = cv.imread(cheminImage,cv.IMREAD_COLOR)
    sift = cv.xfeatures2d.SIFT_create()
    keypoints, descripteurs = sift.detectAndCompute(img,None)

    return descripteurs


def extraireDescripteursEntrainement(nomsImage,cheminImage,nbImg):

    #extraire les descripteurs de toutes les images
    print nomsImage[0]
    dico = descripteurSift(cheminImage + "/" + nomsImage[0])
    print "descripteur 0 "
    print dico[0]
    print dico[-1]
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
        # print descripteurs.shape
        nbDes,tailleDes = descripteurs.shape
        f.ecrireFichierDes(descripteurs,nomsImage[i],cheminRepDes,"/desSift_")


def extraireDico(cheminRepDes,nomsFichierDes,indDIm,indFIm):
    dico = f.extraireDescripteursFichier(cheminRepDes + "/" + nomsFichierDes[indDIm])
    # print "Dico = " + str(dico.shape)
    for i in range(1,indFIm):
        descripteurs = f.extraireDescripteursFichier(cheminRepDes + "/" + nomsFichierDes[i])
        # print "descripteur = " + str(descripteurs.shape)
        dico = np.concatenate((dico,descripteurs))
        # print "Dico = " + str(dico.shape)
    return dico


def calculerClassesDescripteurs(dicoDescripteur,k):
    dico = pd.DataFrame(dicoDescripteur)
    kmeans = KMeans(n_clusters=k).fit(dico)
    print kmeans
    #TODO : Chargement des donnees dans un fichiers pickle
    pickle.dump(kmeans,open("./data/ressources/modeleBOWSIFT.pkl","wb"))
    # return kmeans

def calculerHistogrammeImage(cheminImage,k):
    #TODO extraction kmeans avec pickle
    kmeans = pickle.load(open("./data/ressources/modeleBOWSIFT.pkl","rb"))
    img = cv.imread(cheminImage,cv.IMREAD_COLOR)
    sift = cv.xfeatures2d.SIFT_create()
    keypoints, descripteurs = sift.detectAndCompute(img,None)

    histoG = np.zeros((1,k))
    nbKeypoints = np.size(keypoints)

    for des in descripteurs:
        ind = kmeans.predict([des])
        histoG[0][ind] += 1
    return histoG

def calculerHistogrammeEntrainement(nomsImage,cheminImage,cheminRepDesBOWSIFT,k,nbImg):
    # listeHistoG = []

    for i in range(0,nbImg):
        chemin = cheminImage + "/" + nomsImage[i]
        # listeHistoG.append(calculerHistogrammeImage(chemin,kmeans,k))
        descripteurBOWSIFT = calculerHistogrammeImage(chemin,k)
        f.ecrireFichierDes(descripteurBOWSIFT,nomsImage[i],cheminRepDesBOWSIFT,"/desBOWSift_")
    # return listeHistoG

def listerDesBOWSIFT(cheminRepDesBOWSIFT,nomsFichierBOWSIFT,indDIm,indFIm):

    # desBOWSIFT = f.extraireDesBOWSIFT(cheminRepDesBOWSIFT + "/" + nomsFichierBOWSIFT[indDIm])
    desBOWSIFT = []
    for i in range(0,indFIm):
        descripteur = f.extraireDescripteursFichier(cheminRepDesBOWSIFT + "/" + nomsFichierBOWSIFT[i])
        desBOWSIFT.append(descripteur)

    return desBOWSIFT

def calculerScoresSift(listeHistoG,histoGtest):
    scores = []
    for des in listeHistoG:
        scores.append(distance.euclidean(des,histoGtest))
    return scores
