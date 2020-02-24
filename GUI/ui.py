# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowpython.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.resultsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.resultsTable.setGeometry(QtCore.QRect(230, 140, 551, 391))
        self.resultsTable.setObjectName("resultsTable")
        self.selectVehicleButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectVehicleButton.setGeometry(QtCore.QRect(6, 6, 167, 36))
        self.selectVehicleButton.setObjectName("selectVehicleButton")
        self.startReid = QtWidgets.QPushButton(self.centralwidget)
        self.startReid.setGeometry(QtCore.QRect(179, 6, 176, 36))
        self.startReid.setObjectName("startReid")
        self.img = QtWidgets.QLabel(self.centralwidget)
        self.img.setGeometry(QtCore.QRect(30, 140, 181, 171))
        self.img.setObjectName("img")
        self.imgRes = QtWidgets.QLabel(self.centralwidget)
        self.imgRes.setGeometry(QtCore.QRect(30, 340, 181, 171))
        self.imgRes.setObjectName("imgRes")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Interface de ré-identification"))
        self.selectVehicleButton.setText(_translate("MainWindow", "Séléctionner un véhicule"))
        self.startReid.setText(_translate("MainWindow", "Lancer la réidentification"))
        self.img.setText(_translate("MainWindow", "TextLabel"))
        self.imgRes.setText(_translate("MainWindow", "TextLabel"))
