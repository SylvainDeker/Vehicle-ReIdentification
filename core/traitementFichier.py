def listerContenuFichier(cheminFichier):
        file = open(cheminFichier,"r")
        lines = file.readlines()
        file.close()
        noms = []
        for nom in lines:
            noms.append(str(nom).strip())
        return noms
