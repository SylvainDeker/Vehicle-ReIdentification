import datetime as dt
import numpy as np
import os

def listerContenuFichier(cheminFichier):
        file = open(cheminFichier,"r")
        lines = file.readlines()
        file.close()
        noms = []
        for nom in lines:
            noms.append(str(nom).strip())
        return noms

def listerContenuRep(cheminRep):
    return os.listdir(cheminRep)

def ecrireFichierDes(descripteurs,nomImage,cheminRepDes,debNom):
    nomImage = nomImage.strip(".jpg")
    nomF = debNom + nomImage + ".txt"
    # print cheminRepDes + nomF

    if os.path.exists(cheminRepDes + nomF):
        os.remove(cheminRepDes + nomF)

    fichier = open(cheminRepDes + nomF,"a")

    ligne,colonne = descripteurs.shape

    fichier.write(str(ligne) + "\n" + str(colonne) + "\n")
    for i in range(0,ligne):
        for j in range(0,colonne):
            fichier.write(str(descripteurs[i][j]) + " ")
        fichier.write("\n")

    fichier.close()


def extraireDescripteursFichier(cheminFichierDes):

    file = open(cheminFichierDes,"r")
    lines = file.readlines()
    file.close()

    ligne = int(lines[0].strip("\n"))

    colonne = int(lines[1].strip("\n"))

    des = np.zeros((ligne,colonne))
    for lf in range(2,len(lines)) :
            s = lines[lf].strip("\n")
            v = s.split(" ")
            for c in range(0,colonne):
                    des[lf-2][c] = float(v[c])


    return des
