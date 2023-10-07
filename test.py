from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout)
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400,400,300,300)
    win.setWindowTitle("PyToDo")

    # main code
    label = QtWidgets.QLabel(win)
    label.setText("LISTA DE TAREAS")
    label.adjustSize()
    label.move(100,100)
    # end of main code

    win.show()
    sys.exit(app.exec_())
window()


class PyQtLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):

        Button1 = QPushButton('Up')
        Button2 = QPushButton('Left')
        Button3 = QPushButton('Right')
        Button4 = QPushButton('Down')
        
        grid = QGridLayout()
        grid.addWidget(Button1, 0, 1)
        grid.addWidget(Button2, 1, 0)
        grid.addWidget(Button3, 1, 2)
        grid.addWidget(Button4, 1, 1)

        self.setLayout(grid)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('PyQt5 Layout')
        self.show()
