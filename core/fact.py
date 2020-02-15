import numpy as np
import pickle

import descripteurSift as sift

def initialiserListeImageVehicule():
    # TODO:

    # Charger les descripteurs SIFT
    # Charger les descripteurs CN
    # Charger les descripteur GoogleNet

    #Pour les images de la base d'apprentissage:
        #Créer objet imageVehicle -> ses paramètres + 3 descripteurs récupérés (à 0 par défaut)
        #Ajouter l'objet à la liste
    #retourner la liste
    return null

def calculerFact(imageCherchee,imageRef):
    # TODO:

    #Distances euclidienne entre les 3 descripteurs
    #score = 0.1 * scoreSift + 0.2*scoreCN + 0.3*scoreGoogleNet
    #return score
    return null

def listerScoresFact(imageCherchee,listeImagesRef):
    # TODO:
    #listeFact = []
    #Pour toutes les images de listeImagesRef
        #score = calculerFact(imageChercheenlisteImagesRef[i])
        #listeFact.append((nomImage,score))
    #return listeFact[]
    return null

def trierListeCroissante(listeATrier):
    #TODO:

    #newListe = sorted(listeATrier, key=lambda score: score[1])
    return null
