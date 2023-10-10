import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from sqlite_connect import Communication

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('design/interface.ui', self)

        self.bt_menu.clicked.connect(self.mover_menu)
        # class communication sqlite
        self.base_datos = Communication()
