import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from library3 import Grup, Dish


class MainWindow(QMainWindow):
    """
    Главное окно приложения для управления блюдами.

    Класс отвечает за инициализацию пользовательского интерфейса,
    загрузку данных в таблицу и обработку действий пользователя.
    """

    def __init__(self):
        """
        Инициализация главного окна.

        Загружает пользовательский интерфейс из файла .ui,
        устанавливает заголовок окна, инициализирует группу блюд и
        связывает кнопки с соответствующими методами.
        """
        super(MainWindow, self).__init__() # Вызов инициализатора родительского класса QMainWindow
        loadUi('dish.ui', self)
        self.setWindowTitle("Перделяну Александр")

        # Инициализация группы блюд
        self.group = Grup()
        self.group.read_data("text.txt")
        self.load_table_data()

        # Связывание кнопок с методами
        self.pushButton_add.clicked.connect(self.add_dish)  # Кнопка добавления блюда
        self.pushButton_fill.clicked.connect(self.fill_table)  # Кнопка заполнения таблицы
        self.pushButton_clear.clicked.connect(self.clear_table)  # Кнопка очистки таблицы
        self.pushButton_delete.clicked.connect(self.delete_dish)  # Кнопка удаления блюда
        self.pushButton_delete_cell.clicked.connect(self.delete_cell)  # Кнопка удаления содержимого ячейки
        self.pushButton_edit_cell.clicked.connect(self.edit_cell)  # Кнопка редактирования ячейки
        self.pushButton_save.clicked.connect(self.save_table_data) # Кнопка сохранения тблицы
        
    def load_table_data(self):
        """
        Загрузка данных блюд в таблицу.

        Устанавливает количество колонок, заголовки колонок и заполняет таблицу
        данными из группы блюд.
        """
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
        """
        Добавление нового блюда в таблицу.

        Получает данные блюда из полей ввода, добавляет блюдо в группу
        и обновляет таблицу. Показывает предупреждение в случае ошибки ввода.
        """
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
        """
        Заполнение таблицы данными.

        Вызывает метод загрузки данных в таблицу.
        """
        self.load_table_data()

    def clear_table(self):
        """
        Очистка таблицы.

        Устанавливает количество строк таблицы равным нулю.
        """
        self.tableWidget.setRowCount(0)

    def delete_dish(self):
        """
        Удаление выбранного блюда из таблицы.
        
        Получает выбранную строку, удаляет соответствующее блюдо из группы
        и удаляет строку из таблицы. Показывает сообщение об успешном удалении
        или предупреждение в случае ошибки.
        """
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            name = self.tableWidget.item(selected_row, 0).text()

            if self.group.delete_dish_by_name(name):
                self.tableWidget.removeRow(selected_row)
                QMessageBox.information(self, "Успех", "Блюдо успешно удалено!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить блюдо.")
        else:
            QMessageBox.warning(self, "Ошибка", "Блюдо не выбрано.")

    def delete_cell(self):
        """
        Удаление содержимого выбранной ячейки.
        
        Получает текущую строку и колонку из соответствующих полей ввода,
        удаляет содержимое ячейки и обновляет таблицу.
        """
        current_row = self.spinBox_row.value()
        current_col = self.spinBox_col.value()
        if current_row < self.tableWidget.rowCount() and current_col < self.tableWidget.columnCount():
            self.group.delete_cell(current_row, current_col)
            self.tableWidget.setItem(current_row, current_col, QTableWidgetItem(""))

    def edit_cell(self):
        """
        Редактирование содержимого выбранной ячейки.
        
        Получает текущую строку, колонку и новое значение из соответствующих
        полей ввода, обновляет содержимое ячейки и таблицы.
        Показывает предупреждение в случае ошибки ввода.
        """
        current_row = self.spinBox_row.value()
        current_col = self.spinBox_col.value()
        new_value = self.lineEdit_new_value.text()
        if current_row < self.tableWidget.rowCount() and current_col < self.tableWidget.columnCount():
            if self.group.edit_cell(current_row, current_col, new_value):
                self.tableWidget.setItem(current_row, current_col, QTableWidgetItem(new_value))
            else:
                QMessageBox.warning(self, "Error", "Invalid input data!")

    
    def save_table_data(self):
        """
        Сохранение таблицы в файл save.txt.
        
        Сохраняет данные талицы при нажатии на кнопку "Сохранить".
        """
        row_count = self.tableWidget.rowCount()
        column_count = self.tableWidget.columnCount()
        with open('save.txt', 'w', encoding="utf-8") as file:
            for row in range(row_count):
                row_data = []
                for column in range(column_count):
                    item = self.tableWidget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                file.write(','.join(row_data) + '\n')



if __name__ == "__main__":
    """
    Запуск приложения.
    
    Создает экземпляр QApplication, создает и отображает главное окно,
    запускает цикл обработки событий.
    """
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


