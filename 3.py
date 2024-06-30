import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from library3 import Grup, Dish

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('dish.ui', self)
        self.setWindowTitle("Dish Manager")

        self.group = Grup()
        self.group.read_data("text.txt")  # Загружаем данные сразу
        self.load_table_data()

        # Привязка кнопок
        self.pushButton_3.clicked.connect(self.add_dish)
        self.pushButton.clicked.connect(self.fill_table)
        self.pushButton_2.clicked.connect(self.clear_table)
        self.pushButton_delete.clicked.connect(self.delete_dish)
        self.pushButton_delete_cell.clicked.connect(self.delete_cell)
        self.pushButton_edit_cell.clicked.connect(self.edit_cell)

    def load_table_data(self):
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Dish Name", "Category", "Weight", "Cost"])
        self.tableWidget.setRowCount(len(self.group.A))

        for row, dish in enumerate(self.group.A):
            print(f"Loading row {row}: {dish}")  # Отладочное сообщение
            self.tableWidget.setItem(row, 0, QTableWidgetItem(dish.name))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(dish.category))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(dish.weight)))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(dish.cost)))

    def add_dish(self):
        name = self.lineEdit_name.text()
        category = self.lineEdit_category.text()
        weight = self.lineEdit_weight.text()
        cost = self.lineEdit_cost.text()

        if self.group.append_dish(name, category, weight, cost):
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(category))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(weight))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(cost))
        else:
            QMessageBox.warning(self, "Error", "Invalid input data!")

    def fill_table(self):
        self.load_table_data()  # Заполняем таблицу данными

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def delete_dish(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            name = self.tableWidget.item(selected_row, 0).text()
            category = self.tableWidget.item(selected_row, 1).text()
            cost = self.tableWidget.item(selected_row, 3).text()

            if self.group.delete_dish_by_name(name):
                self.tableWidget.removeRow(selected_row)
                QMessageBox.information(self, "Успех", "Блюдо успешно удалено!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить блюдо.")
        else:
            QMessageBox.warning(self, "Ошибка", "Блюдо не выбрано.")


    def delete_cell(self):
        current_row = self.spinBox_row.value()
        current_col = self.spinBox_col.value()
        if current_row < self.tableWidget.rowCount() and current_col < self.tableWidget.columnCount():
            self.group.delete_cell(current_row, current_col)
            self.tableWidget.setItem(current_row, current_col, QTableWidgetItem(""))

    def edit_cell(self):
        current_row = self.spinBox_row.value()
        current_col = self.spinBox_col.value()
        new_value = self.lineEdit_new_value.text()
        if current_row < self.tableWidget.rowCount() and current_col < self.tableWidget.columnCount():
            if self.group.edit_cell(current_row, current_col, new_value):
                self.tableWidget.setItem(current_row, current_col, QTableWidgetItem(new_value))
            else:
                QMessageBox.warning(self, "Error", "Invalid input data!")

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())
