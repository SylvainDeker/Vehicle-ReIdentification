import sys
import os
from PySide2 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.text = QtWidgets.QLabel()

        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.colorSelector = QtWidgets.QColorDialog()
        self.colorSelector.setOptions(QtWidgets.QColorDialog.NoButtons)
        self.layout = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton("OK")

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.colorSelector)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)
        app.aboutToQuit.connect(self.closeEvent)

    def closeEvent(self):
        #Your desired functionality here
        # print('Close button pressed')
        sys.exit(0)

    def majimg(self,imgpath):

        self.imgpath = imgpath
        pixmap = QtGui.QPixmap(imgpath)
        self.text.setPixmap(pixmap)


    def magic(self):
        r,g,b,_ = self.colorSelector.currentColor().getRgb()
        print("\"" + self.imgpath+"\"," + str(r) + ","+ str(g) + ","+ str(b))
        self.closeEvent()


from ExtractColorTest import indexJPG
if __name__ == "__main__":
    if str(sys.argv[1])=="folder":
        list = indexJPG("../data/VeRi_with_plate/testperso/manual/",100000)
        for i in range(len(list)):
            cmd = "python3 ColorDefiner.py "+list[i]
            os.system(cmd)
            # print(cmd)
    
    else:
        app = QtWidgets.QApplication([])
        widget = MyWidget()
        widget.resize(800, 600)
        widget.majimg(sys.argv[1])
        widget.show()
        sys.exit(app.exec_())
