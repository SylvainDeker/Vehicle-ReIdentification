import descripteurSift as dSift
import traitementFichier as f

import numpy as np
import os
import time


def testerCreationDicoV1():
    debut = time.time()
    dico = dSift.extraireDescripteursEntrainement(nomsImage,cheminImage,nbImgTester)
    fin = time.time()

    print "\tTemps de calcul du dictionnaire sift: " + str(fin-debut) + " secondes\n"
    print ("Taille du dictionnaire = " + str(dico.shape) + "\n")
    print "Type du dictionnaire : " + str(type(dico))

def testerCreationFichiersDes(cheminImage,cheminRepDes,indDIm,indFIm,nomsImage):
    ##Creation fichiers des descripteurs de chaque image
    debut = time.time()
    dSift.creerFichiersDico(nomsImage,cheminImage,cheminRepDes,indDIm,indFIm)
    nomsFichierDes = f.listerContenuRep(cheminRepDes)
    print len(nomsFichierDes)
    print "Nb de fichier = " + str(len(nomsFichierDes))
    fin = time.time()
    print "\tTemps de calcul des descripteurs Sift par image : " + str(fin-debut) + " secondes\n"
    return nomsFichierDes

def testerExtractionDictionnaire(cheminRepDes,nomsFichierDes,indDIm,indFIm,pas):
    debut = time.time()
    dico = dSift.extraireDico(cheminRepDes,nomsFichierDes,indDIm,indFIm,pas)
    fin = time.time()
    print "Temps d'extraction des valeurs pour creation du dictionnaire" + str(fin-debut) + "secondes"
    print ("Taille du dictionnaire = " + str(dico.shape) + "\n")
    print type(dico)
    return dico

def testerKMeans(dico,k,bs):
    #Creation du Modele d'apprentissage non supervise
    debut = time.time()
    dSift.calculerClassesDescripteurs(dico,k,bs)
    fin = time.time()
    print "\tTemps de calcul des k centroides : " + str(fin-debut) + " secondes\n"
    # return kmeans

def testerCalculHistoGSift(nomsImage,cheminImage,cheminRepDesBOWSIFT,k,kmeans,nbImgTester):
        debut = time.time()
        dSift.calculerHistogrammeEntrainement(nomsImage,cheminImage,cheminRepDesBOWSIFT,kmeans,k,nbImgTester)
        fin = time.time()

        print "\tTemps de calcul des" + str(nbImgTester) + "descripteurs BOW-SIFT  : " + str(fin-debut) + " secondes\n"
        nomsFichierBOWSIFT = f.listerContenuRep(cheminRepDesBOWSIFT)
        print "Nb de fichier = " + str(len(nomsFichierBOWSIFT))

        return nomsFichierBOWSIFT

def testerExtraireBOWSIFT(cheminRepDesBOWSIFT,nomsFichierBOWSIFT,indDIm,indFIm,pas):
    debut = time.time()
    listeHistoG = dSift.listerDesBOWSIFT(cheminRepDesBOWSIFT,nomsFichierBOWSIFT,indDIm,indFIm,pas)
    fin = time.time()
    print "\tTemps d'extraction des" + str(indFIm) + "descripteurs BOW-SIFT  : " + str(fin-debut) + " secondes\n"
    print "Nb histoG " + str(len(listeHistoG)) + " = Nombre d'image " + str(indFIm)
    print "Nb classe histoG = " + str(np.size(listeHistoG[0]))
    # print listeHistoG
    return listeHistoG


def testerReconnaissanceImage(cheminTest,kmeans,k):
        #Tester la reconnaissance image
        debut = time.time()
        histoGtest = dSift.calculerHistogrammeImage(cheminTest,,kmeans,k)
        fin = time.time()
        print "\tTemps de calcul du descripteur BOW-SIFT de l'image test : " + str(fin-debut) + " secondes\n"
        return histoGtest

def testerCalculScoreSift(listeHistoG,histoGtest):
        debut = time.time()
        scores = []
        for i in range(0,len(listeHistoG)):
            scores.append(dSift.calculerScoresSift(listeHistoG,histoGtest))
        fin = time.time()
        print "\tTemps de calcul des scores de distance euclidienne : " + str(fin-debut) + " secondes\n"
        print scores
        return scores

def testerFonctionsSift():
    cheminImage = '../data/VeRi_with_plate/image_train'
    cheminFichier = '../data/VeRi_with_plate/name_train.txt'
    cheminTest = '../data/VeRi_with_plate/image_test/0002_c002_00030600_0.jpg'
    cheminRepDes = '../data/ressources/descripteursSift'
    cheminRepDesBOWSIFT = '../data/ressources/descripteursBOWSift'
    indDIm = 0
    indFIm = len(os.listdir(cheminImage))
    pas = 4
    k = 10000
    bs = (indFIm / pas) * 3
    nomsImage = f.listerContenuFichier(cheminFichier)

    nomsFichierDes = testerCreationFichiersDes(cheminImage,cheminRepDes,indDIm,indFIm,nomsImage)
    # nomsFichierDes = f.listerContenuRep(cheminRepDes)
    dico = testerExtractionDictionnaire(cheminRepDes,nomsFichierDes,indDIm,indFIm,pas)

    testerKMeans(dico,k,bs)
    # kmeans = pickle.load(open("../data/ressources/modeleBOWSIFT.pkl","rb"))

    nomsFichierBOWSIFT = testerCalculHistoGSift(nomsImage,cheminImage,cheminRepDesBOWSIFT,kmeans,k,indFIm)
    # nomsFichierBOWSIFT = os.listdir(cheminRepDesBOWSIFT)
    listeHistoG = testerExtraireBOWSIFT(cheminRepDesBOWSIFT,nomsFichierBOWSIFT,indDIm,indFIm,pas)

    histoGtest = testerReconnaissanceImage(cheminTest,kmeans,k)

    scores = testerCalculScoreSift(listeHistoG,histoGtest)

#main
testerFonctionsSift()
