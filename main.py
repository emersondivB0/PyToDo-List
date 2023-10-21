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
        # Initialize in page 1
        self.stackedWidget.setCurrentIndex(1)

        self.bt_menu.clicked.connect(self.mover_menu)
        # class communication sqlite
        self.base_datos = Communication()

        # Hide buttons
        self.bt_show_main.clicked.connect(self.show_tasks)
        self.bt_refresh.clicked.connect(self.show_tasks)
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
        self.bt_add_main.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_add)
        )
        self.bt_show_main.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_show)
        )
        self.bt_delete_main.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_delete)
        )
        self.bt_edit_main.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_edit)
        )

        # Column width
        self.table_delete.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_tasks.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    # Sizegrp :
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize
        )

    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def move_window(self, event):
        if self.isMaximized() is False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()

    # Resize menu Column
    def mover_menu(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animation = QPropertyAnimation(
                self.frame_control, b'minimumWidth'
            )
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extender)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    # Database page
    def show_tasks(self):
        datos = self.base_datos.show_tasks()
        i = len(datos)
        self.table_tasks.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.table_tasks.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(row[1])
            )
            self.table_tasks.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(row[2])
            )
            self.table_tasks.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(row[3])
            ) 
            tablerow += 1
            self.signal_list.setText('')
            self.signal_delete.setText('')
            self.signal_edit.setText('')
            self.signal_add.setText('')

    def add_task(self):
        name = self.add_name.text().upper()
        description = self.add_description.text().upper()
        finnished = 0
        end_date = self.add_date.text().upper()
        if name != '' and description != '' and end_date != '':
            self.base_datos.add_task(name, description, end_date, finnished)
            self.signal_add.setText('Tasks Added!')
            self.add_name.clear()
            self.add_description.clear()
            self.add_date.clear()
        else:
            self.signal_add.setText('Thereare white spaces!')

    def find_by_name_search(self):
        id_task = self.edit_search.text().upper()
        id_task = str("'" + id_task + "'")
        self.task = self.base_datos.search_task(id_task)
        if len(self.task) != 0:
            self.Id = self.task[0][0]
            self.edit_name.setText(self.task[0][1])
            self.edit_description.setText(self.task[0][2])
            self.edit_date.setText(self.task[0][3])

    def edit_task(self):
        if self.task != '':
            name = self.edit_name.text().upper()
            description = self.edit_description.text().upper()
            end_date = self.edit_date.text().upper()
            act = self.base_datos.edit_task(
                self.Id, name, description, end_date
            )
            if act == 1:
                self.signal_edit.setText('Updated!')
                self.edit_name.clear()
                self.edit_description.clear()
                self.edit_date.clear()
                self.edit_search.setText('')
            elif act == 0:
                self.signal_edit.setText('ERROR!')
            else:
                self.signal_edit.setText('WRONG!')

    def find_by_name_delete(self):
        name_product = self.delete_search.text().upper()
        name_product = str("'" + name_product + "'")
        product = self.base_datos.search_task(name_product)
        self.table_delete.setRowCount(len(product))

        if len(product) == 0:
            self.signal_delete.setText("Doesn't Exist!")
        else:
            self.signal_delete.setText('Task selected!')
        tablerow = 0
        for row in product:
            self.task_to_delete = row[1]
            self.table_delete.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(row[1])
            )
            self.table_delete.setItem(
                tablerow, 1, QtWidgets.QTableWidgetItem(row[2])
            )
            self.table_delete.setItem(
                tablerow, 2, QtWidgets.QTableWidgetItem(row[3])
            )
            tablerow += 1

    def delete_task(self):
        self.row_flag = self.table_delete.currentRow()
        if self.row_flag == 0:
            self.table_delete.removeRow(0)
            self.base_datos.delete_task("'" + self.task_to_delete + "'")
            self.signal_delete.setText('Task deleted!')
            self.delete_search.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = VentanaPrincipal()
    my_app.show()
    sys.exit(app.exec_())
