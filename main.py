# CRUD with PyQt5 and SQLite3
# @Author: emersondivB0
# GitHub: https://github.com/emersondivB0

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget
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

        # Hide buttons
        self.bt_show_main.clicked.connect(self.show_tasks)
        self.bt_add.clicked.connect(self.add_task)
        self.bt_delete.clicked.connect(self.delete_task)
        self.bt_edit.clicked.connect(self.edit_task)
        self.bt_edit_search.clicked.connect(self.find_by_name_search)
        self.bt_search_delete.clicked.connect(self.find_by_name_delete)

        # Title bar control
        self.setWindowOpacity(1)

        # Sizegrip - redimention
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Connection buttons
        self.bt_add_main.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(
            self.page_add))
        self.bt_show_main.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(
            self.page_show))
        self.bt_delete_main.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(
            self.page_delete))
        self.bt_edit_main.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(
            self.page_edit))

        # Column width
        self.table_delete.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_tasks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #Sizegrp :
        def resizeEvent(self, event):
            rect = self.rect()
            self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

        def mousePressEvent(self, event):
            self.click_position = event.globalPos()

        def move_window(self, event):
            if self.isMaximized() == False:
                if event.buttons() == QtCore.Qt.LefButton:
                    self.move(self.pos() + event.globalPos() - self.click_position)
                    self.click_position = event.globalPos()
                    event.accept()
        
        #Resize menu Column
        def mover_menu(self):
            if True:
                width = self.frame_control.width()
                normal = 0
                if width==0:
                    extender = 200
                else:
                    extender = normal
                self.animation = QPropertyAnimation(self.frame_control, b'minimumWidth')
                self.animation.setDuration(300)
                self.animation.setStartValue(width)
                self.animation.setEndValue(extender)
                self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation.start()

        #Database page
        def show_tasks(self):
            datos = self.base_datos.show_tasks() 
