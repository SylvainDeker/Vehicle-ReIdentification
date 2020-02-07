import sys
from PyQt5 import QtCore,QtWidgets,QtGui, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

from ui import Ui_MainWindow


def changeLabelImage(widget,fileLocation):
    pixmap = QPixmap(fileLocation)
    widget.setPixmap(pixmap)

def initTableResult(table,n,):
    table.setRowCount(numberOfResultsToDisplay)
    table.setColumnCount(4)
    labels=['Id véhicule','Id caméra','Nom du fichier','Score']
    table.setHorizontalHeaderLabels(labels)
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    window.resultsTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

def fillLineTable(table,line,data0,data1,data2,data3):
    table.setItem(line,0, QTableWidgetItem(data0))
    table.setItem(line,1, QTableWidgetItem(data1))
    table.setItem(line,2, QTableWidgetItem(data2))
    table.setItem(line,3, QTableWidgetItem(data3))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

numberOfResultsToDisplay = 3
resultsFile = './resultats.xml'


changeLabelImage(window.img,'./0001_c001_00016450_0.jpg')
changeLabelImage(window.imgRes,'./0003_c001_00021480_0.jpg')

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




window.show()
app.exec()
