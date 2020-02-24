from ColorName import ColorName
import googleNet as gn
import descripteurSift as sift
import time
import pickle

def calculerFact(scoreCN,scoreSift,scoreGoogleNet):

    score = 0.1 * scoreSift + 0.2*scoreCN + 0.7*scoreGoogleNet

    return score


def listerScoresFact(imageCherchee,listeImagesRef,listeDesBOWSIFT,featureExtractor):
    listeFact = []

    #Calcul score de distance GoogleNet
    debut = time.time()
    listeGoogleNet = gn.googleNetScore(imageCherchee,featureExtractor)
    fin = time.time()
    print ("\nTemps de calcul des scores googleNet : " + str(fin-debut) + " secondes")

    #Calcul du score de distance entre les deux descripteurs BOWSIFT
    debut = time.time()
    kmeans = pickle.load(open("../data/ressources/modeleBOWSIFT.pkl","rb"))
    fin = time.time()
    print ("Temps de chargement du modele kmoyenne BOWSIFT : " + str(fin-debut) + " secondes")
    debut = time.time()
    desBOWSIFT = sift.calculerHistogrammeImage(imageCherchee,kmeans,10000)
    listeScoresSift = sift.calculerScoresSift(listeDesBOWSIFT,desBOWSIFT)
    fin = time.time()
    print ("Temps de calcul des scores BOWSIFT : " + str(fin-debut) + " secondes\n")

    for i in range(0,len(listeImagesRef),10):
        scoreGoogleNet, nomIm  = listeGoogleNet[i]
        # scoreGoogleNet = 0

        cn = ColorName()
        cn.loadimgref( '../data/VeRi_with_plate/image_train/' + listeImagesRef[i])
        # retourne un score entre 0 et 1, 1 = ressemblance absolue
        scoreCN = cn.compareTo(imageCherchee)

        score = calculerFact(scoreCN,listeScoresSift[i],scoreGoogleNet)
        listeFact.append((listeImagesRef[i],score))
#        print i

    return listeFact


def trierListeCroissante(listeATrier):
    newListe = sorted(listeATrier, key=lambda score: score[1])
    return newListe
