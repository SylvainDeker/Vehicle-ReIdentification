from ColorName import ColorName
import googleNet as gn
import descripteurSift as sift
import time
import pickle

def calculerFact(scoreCN,scoreSift,scoreGoogleNet):

    score = 0.1 * scoreSift + 0.2*scoreCN + 0.7*scoreGoogleNet

    return score


def listerScoresFact(imageCherchee,listeImagesRef,listeDesBOWSIFT,featureExtractor,pas):
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

    googleNetTrie = sorted(listeGoogleNet, key=lambda nom: nom[1])
    siftTrie = sorted(listeScoresSift, key=lambda nom: nom[1])

    for i in range(0,len(listeImagesRef),pas):
        scoreGoogleNet, nomIm  = googleNetTrie[i]

        scoreSift , nomImS = siftTrie[i]
        # scoreSift = 0
        cn = ColorName()
        cn.loadimgref( '../data/VeRi_with_plate/image_train/' + nomIm)
        # retourne un score entre 0 et 1, 1 = ressemblance absolue
        scoreCN = 1-cn.compareTo(imageCherchee)
        # scoreCN = 0

        score = calculerFact(scoreCN,scoreSift,scoreGoogleNet)
        listeFact.append((nomIm,score))
        print (str(i) + " -> " + nomIm)
    return listeFact


def trierListeCroissante(listeATrier):
    newListe = sorted(listeATrier, key=lambda score: score[1])
    return newListe
