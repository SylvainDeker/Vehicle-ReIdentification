import sys
sys.path.append('../core/')
import fact
import descripteurSift as sift
import traitementFichier as f
import googleNet as gn
import testsFact as tF

import time
import pickle

from PyQt5 import QtCore,QtWidgets,QtGui, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QFileDialog,QInputDialog,QLineEdit
from PyQt5.QtCore import pyqtSlot

from ui import Ui_MainWindow

#Cette fonction prend en parametre : un label et une location d une image
#Elle modifie le background du label avec l'image
def changeLabelImage(widget,fileLocation):
    pixmap = QPixmap(fileLocation)
    widget.setPixmap(pixmap)

#Cette fonction prend en parametre : un tableau et un entier
#Elle initialise le tableau avec le nombre de ligne = l'entier
#Elle initialise egalement la partie colonne et gere l'edition des valeurs
def initTableResult(table,n):
    table.setRowCount(n)
    table.setColumnCount(4)
    labels=['Id vehicule','Id camera','Nom du fichier','Score']
    table.setHorizontalHeaderLabels(labels)
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    window.resultsTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

#Cette fonction prend en parametre : un tableau , un entier et 4 donnees
#Elle initialise la ligne(entier) du tableau avec les donnees fournit
def fillLineTable(table,line,data0,data1,data2,data3):
    table.setItem(line,0, QTableWidgetItem(data0))
    table.setItem(line,1, QTableWidgetItem(data1))
    table.setItem(line,2, QTableWidgetItem(data2))
    table.setItem(line,3, QTableWidgetItem(data3))

def openFileNameDialog():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global fileName
        fileName, _ = QFileDialog.getOpenFileName(window,"Selectionner un vehicule", "","Images files (*.jpg)", options=options)
        if fileName:
            print(fileName)
            changeLabelImage(window.img,fileName)
            window.startReid.setEnabled(True)

def reIdentificationPlaceHolder():
    print('Lancement de la reidentification')
    print("2{}".format(fileName))
    listeFactTriee = tF.testerFact(fileName,nomsImage,listeDesBOWSIFT,featureExtractor,4)

    #Si on a moins de resultas que le nombre de top(1 ou 3 ou 5)
    if len(listeFactTriee)>numberOfResultsToDisplay:
        max=numberOfResultsToDisplay
    else:
        max=len(listeFactTriee)

    initTableResult(window.resultsTable,max)

    for i in range(0,max):
        data = listeFactTriee[i][0].split('_')
        print(listeFactTriee[i][1])
        score = str(listeFactTriee[i][1])[:4]
        fillLineTable(window.resultsTable,i,data[0],data[1],listeFactTriee[i][0],score)

def displayResultImage():
    row = window.resultsTable.currentRow() # Index of Row
    firstColumnInRow = window.resultsTable.item(row, 2) # returns QTableWidgetItem
    text = firstColumnInRow.text() # content of this
    changeLabelImage(window.imgRes,cheminImage+'/'+text)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.selectVehicleButton.clicked.connect(openFileNameDialog)
        self.startReid.clicked.connect(reIdentificationPlaceHolder)
        self.resultsTable.clicked.connect(displayResultImage)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

cheminImage = '../data/VeRi_with_plate/image_train'
cheminFichier = '../data/VeRi_with_plate/name_train.txt'
cheminRepDesBOWSIFT = '../data/ressources/descripteursBOWSift'
indDIm = 0
indFIm = len(f.listerContenuFichier(cheminFichier))
pas = 4
# global fileName
fileName = ""

nomsImage = f.listerContenuFichier(cheminFichier)
nomsFichierBOWSIFT = f.listerContenuRep(cheminRepDesBOWSIFT)
debut = time.time()
listeDesBOWSIFT = pickle.load(open("../data/ressources/listeDesBOWSIFT.pkl","rb"))

fin = time.time()
print ("Temps de chargement de la liste des descripteurs BOW-SIFT : " + str(fin-debut) + " secondes")

debut = time.time()
featureExtractor = gn.initModel()
fin = time.time()
print ("Temps de chargement du modele GoogleNet : " + str(fin-debut) + " secondes")


changeLabelImage(window.img,'./placeholder2.png')
changeLabelImage(window.imgRes,'./placeholder2.png')
window.startReid.setEnabled(False)

numberOfResultsToDisplay = 15
resultsFile = './resultats.xml'

window.show()
app.exec_()
