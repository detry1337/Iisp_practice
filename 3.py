import library3 as lib
import sys
from PyQt5 import QtWidgets
from dish_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gr = lib.Grup()
        self.gr.read_data("text.txt")
        self.pushButton.clicked.connect(self.fill_table)
        self.pushButton_2.clicked.connect(self.clear_table)
        
    def fill_table(self):
        self.tableWidget.setRowCount(len(self.gr.A))
        for row, dish in enumerate(self.gr.A):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(dish.name))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(dish.category))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(dish.weight)))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(dish.cost)))

    def clear_table(self):
        self.tableWidget.clearContents()

def main():
    Gr = lib.Grup()
    Gr.read_data("text.txt")
    print("Меню:", Gr)
    
    while True:
        print("Выберите действие:")
        print("1. Вывести данные блюд категории X в файл")
        print("2. Сформировать список блюд категории X по стоимости и вывести его")
        print("3. Выполнить поиск блюда в списке L")
        print("4. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            category = input("Введите категорию блюд для записи в файл: ")
            file_name = input("Введите имя файла для записи: ")
            lib.write_category(category, Gr.menu_dict, file_name)
            print(f"Данные блюд категории {category} записаны в файл {file_name}.")

        elif choice == "2":
            category = input("Введите категорию блюд для формирования списка: ")
            max_price = int(input("Введите максимальную стоимость блюд: "))
            sorted_dishes = lib.filter_and_sort_dishes(category, max_price, Gr.menu_dict)
            for dish in sorted_dishes:
                print(dish)

        elif choice == "3":
            category = input("Введите категорию блюд для формирования списка: ")
            max_price = int(input("Введите максимальную стоимость блюд: "))
            sorted_dishes = lib.filter_and_sort_dishes(category, max_price, Gr.menu_dict)
            dish_name = input("Введите название блюда для поиска: ")
            search_result = lib.linear_search(dish_name, sorted_dishes)
            if search_result:
                print(f"Найдено блюдо: {search_result}")
            else:
                print("Блюдо не найдено.")

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())