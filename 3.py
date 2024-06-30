import sys
from PyQt5 import QtWidgets
import library3 as lib
from dish_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gr = lib.Grup()
        self.gr.read_data("text.txt")
        self.pushButton.clicked.connect(self.fill_table)
        self.pushButton_2.clicked.connect(self.clear_table)
        self.pushButton_3.clicked.connect(self.append_dish)  # Подключаем кнопку для добавления блюда

    def fill_table(self):
        self.tableWidget.setRowCount(len(self.gr.A))
        for row, dish in enumerate(self.gr.A):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(dish.name))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(dish.category))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(dish.weight)))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(dish.cost)))

    def clear_table(self):
        self.tableWidget.clearContents()

    def append_dish(self):
        name = self.lineEdit_name.text()
        category = self.lineEdit_category.text()
        weight = self.lineEdit_weight.text()
        cost = self.lineEdit_cost.text()

        result = self.gr.append_dish(name, category, weight, cost)
        if result:
            self.fill_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось добавить блюдо. Проверьте корректность данных.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
