import fact
import descripteurSift as sift
import traitementFichier as f
import googleNet as gn
import pickle
import time

def testerFact(imageCherchee,listeImagesRef,listeDesBOWSIFT,featureExtractor,pas):
    debut = time.time()
    listeFact = fact.listerScoresFact(imageCherchee,listeImagesRef,listeDesBOWSIFT,featureExtractor,pas)
    fin = time.time()

    print ("Temps de calcul des " + str(len(listeImagesRef)) + " scores Fact : " + str(fin-debut))

    debut = time.time()
    listeFactTriee = fact.trierListeCroissante(listeFact)
    fin = time.time()

    print ("Temps de trie de la liste de score " + str(fin-debut))

    return listeFactTriee

#Main de test du module fact
# cheminImage = '../data/VeRi_with_plate/image_train'
# cheminFichier = '../data/VeRi_with_plate/name_train.txt'
# cheminTest = '../data/VeRi_with_plate/image_test/0006_c014_00024880_0.jpg'
# cheminRepDesBOWSIFT = '../data/ressources/descripteursBOWSift'
# indDIm = 0
# indFIm = len(f.listerContenuFichier(cheminFichier))
# pas = 1
# #
# # nomsImage = f.listerContenuFichier(cheminFichier)
# nomsFichierBOWSIFT = f.listerContenuRep(cheminRepDesBOWSIFT)
#
# listeDesBOWSIFT = sift.listerDesBOWSIFT(cheminRepDesBOWSIFT,nomsFichierBOWSIFT,indDIm,indFIm,pas)
#
# pickle.dump(listeDesBOWSIFT,open("../data/ressources/listeDesBOWSIFT.pkl","wb"))
# debut = time.time()

# listeDesBOWSIFT = pickle.load(open("../data/ressources/listeDesBOWSIFT.pkl","rb"))
# fin = time.time()
# print ("Temps de chargement de la liste des descripteurs BOW-SIFT : " + str(fin-debut) + " secondes")
#
# debut = time.time()
# featureExtractor = gn.initModel()
# gn.prepareSemanticDataSet(featureExtractor)
# fin = time.time()
# print ("Temps de chargement du modele GoogleNet : " + str(fin-debut) + " secondes")
#
# listeFactTriee = testerFact(cheminTest,nomsImage,listeDesBOWSIFT,featureExtractor,pas)
#
# for i in range(0,10):
#     print (listeFactTriee[i])
