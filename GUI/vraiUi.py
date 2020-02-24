import sys
from PyQt5 import QtCore,QtWidgets,QtGui, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QFileDialog,QInputDialog,QLineEdit
from PyQt5.QtCore import pyqtSlot

from ui import Ui_MainWindow

#Cette fonction prend en paramètre : un label et une location d'une image
#Elle modifie le background du label avec l'image
def changeLabelImage(widget,fileLocation):
    pixmap = QPixmap(fileLocation)
    widget.setPixmap(pixmap)

#Cette fonction prend en paramètre : un tableau et un entier
#Elle initialise le tableau avec le nombre de ligne = l'entier
#Elle initialise également la partie colonne et gère l'édition des valeurs
def initTableResult(table,n):
    table.setRowCount(n)
    table.setColumnCount(4)
    labels=['Id véhicule','Id caméra','Nom du fichier','Score']
    table.setHorizontalHeaderLabels(labels)
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    window.resultsTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

#Cette fonction prend en paramètre : un tableau , un entier et 4 données
#Elle initialise la ligne(entier) du tableau avec les données fournit
def fillLineTable(table,line,data0,data1,data2,data3):
    table.setItem(line,0, QTableWidgetItem(data0))
    table.setItem(line,1, QTableWidgetItem(data1))
    table.setItem(line,2, QTableWidgetItem(data2))
    table.setItem(line,3, QTableWidgetItem(data3))

def openFileNameDialog():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(window,"Sélectionner un véhicule", "","Images files (*.jpg)", options=options)
        if fileName:
            print(fileName)
            changeLabelImage(window.img,fileName)
            window.startReid.setEnabled(True)

def reIdentificationPlaceHolder():
    print('Lancement de la réidentification')
    #On lit les résultats dans le fichier
    #Les résultats sont stockés sous la forme tableau de tableau
    #Les sous tableaux sont constitués de 2 éléments : le nom de fichier et sa distance FACT à l'image source
    fileLine=0
    fileData = []
    with open(resultsFile, "r") as f:
        for line in f.readlines():
            fileLine+=1
            fileData+=[(line.rstrip('\n')).split()]

    #Si on à moins de résultas que le nombre de top(1 ou 3 ou 5)
    if fileLine>numberOfResultsToDisplay:
        max=numberOfResultsToDisplay
    else:
        max=fileLine

    #print(fileData[0])
    initTableResult(window.resultsTable,max)

    for i in range(0,max):
        data = fileData[i][0].split('_')
        print(fileData[i][1])
        fillLineTable(window.resultsTable,i,data[0],data[1],fileData[i][0],fileData[i][1])

def displayResultImage():
    row = window.resultsTable.currentRow() # Index of Row
    firstColumnInRow = window.resultsTable.item(row, 2) # returns QTableWidgetItem
    text = firstColumnInRow.text() # content of this
    changeLabelImage(window.imgRes,'./'+text)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.selectVehicleButton.clicked.connect(openFileNameDialog)
        self.startReid.clicked.connect(reIdentificationPlaceHolder)
        self.resultsTable.clicked.connect(displayResultImage)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

changeLabelImage(window.img,'./placeholder2.png')
changeLabelImage(window.imgRes,'./placeholder2.png')
window.startReid.setEnabled(False)

numberOfResultsToDisplay = 3
resultsFile = './resultats.xml'

window.show()
app.exec()
