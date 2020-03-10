from PySide2 import QtCore,QtWidgets,QtGui
import sys
import random

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello=["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button=QtWidgets.QPushButton('click me')
        self.button.setToolTip('this is a <b>map query button<b>')

        self.text = QtWidgets.QLabel("Hello World")
        self.setWindowTitle("first demo")
        self.text.setAlignment(QtCore.Qt.AlignLeft)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def magic(self):
        newindow = SecondWidget()
        newindow.show()
        newindow.exec_()




class SecondWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.newWindowUI
        self.setWindowTitle('second window')
        self.button=QtWidgets.QPushButton("click and query")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        #self.button.clicked.connect(self.on_clicked())
    def newWindowUI(self):
        self.resize(400,300)
        #self.move(200,200)
    def on_clicked(self):
        alert=QtWidgets.QMessageBox()
        alert.setText('lalalalal')
        alert.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(500, 400)
    widget.show()

    sys.exit(app.exec_())