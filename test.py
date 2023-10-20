import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from sqlite_connect import Communication

class TaskTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(TaskTableModel, self).__init__(parent)
        self.tasks = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.tasks)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            task = self.tasks[index.row()]
            if index.column() == 0:
                return task[1]
            elif index.column() == 1:
                return task[2]
            elif index.column() == 2:
                return task[3]
            elif index.column() == 3:
                return task[4]
        return None

    def fetchTasks(self):
        self.beginResetModel()
        self.tasks = self.parent().base_datos.show_tasks()
        self.endResetModel()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('design/interface.ui', self)

        self.bt_menu.clicked.connect(self.mover_menu)
        self.base_datos = Communication()

        self.bt_show_main.clicked.connect(self.show_tasks)
        self.bt_add.clicked.connect(self.add_task)
        self.bt_delete.clicked.connect(self.delete_task)
        self.bt_edit.clicked.connect(self.edit_task)
        self.bt_edit_search.clicked.connect(self.find_by_name_search)
        self.bt_search_delete.clicked.connect(self.find_by_name_delete)

        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

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

        self.table_delete.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_tasks.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.taskTableModel = TaskTableModel(self)
        self.table_tasks.setModel(self.taskTableModel)

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

    def mover_menu(self):
        width = self.frame_control.width()
        normal = 0
        extender = 200 if width == 0 else normal
        self.animation = QPropertyAnimation(
            self.frame_control, b'minimumWidth'
        )
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(extender)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def show_tasks(self):
        self.taskTableModel.fetchTasks()

    def add_task(self):
        name = self.add_name.text().upper()
        description = self.add_description.text().upper()
        end_date = self.add_date.text().upper()
        if all([name, description, end_date]):
            self.base_datos.add_task(name, description, end_date, 0)
            self.signal_add.setText('Tasks Added!')
            self.add_name.clear()
            self.add_description.clear()
            self.add_date.clear()
        else:
            self.signal_add.setText('There are white spaces!')

    def find_by_name_search(self):
        id_task = self.edit_search.text().upper()
        self.task = self.base_datos.search_task(id_task)
        if self.task:
            self.Id = self.task[0][0]
            self.edit_name.setText(self.task[0][1])
            self.edit_description.setText(self.task[0][2])
            self.edit_date.setText(self.task[0][3])

    def edit_task(self):
        if self.task:
            name = self.edit_name.text().upper()
            description = self.edit_description.text().upper()
            end_date = self.edit_date.text().upper()
            finished = 0
            act = self.base_datos.edit_task(
                self.Id, name, description, end_date, finished
            )
            if act:
                self.signal_edit.setText('Updated!')
                self.edit_name.clear()
                self.edit_description.clear()
                self.edit_date.clear()
                self.edit_search.setText('')
            else:
                self.signal_edit.setText('ERROR!')

    def find_by_name_delete(self):
        name_product = self.delete_search.text().upper()
        product = self.base_datos.search_task(name_product)
        self.table_delete.setRowCount(len(product))

        if not product:
            self.signal_delete.setText("Doesn't Exist!")
        else:
            self.signal_delete.setText('Task selected!')
        for row, task in enumerate(product):
            self.task_to_delete = task[1]
            self.table_delete.setItem(
                row, 0, QtWidgets.QTableWidgetItem(task[1])
            )
            self.table_delete.setItem(
                row, 1, QtWidgets.QTableWidgetItem(task[2])
            )
            self.table_delete.setItem(
                row, 2, QtWidgets.QTableWidgetItem(task[3])
            )

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
