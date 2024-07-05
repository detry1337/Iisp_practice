class Dish:
    """
    Класс для представления блюда.

    Содержит информацию о названии, категории, весе и стоимости блюда.
    """

    def __init__(self, name="", category="", weight=None, cost=None):
        """
        Инициализация экземпляра класса Dish.

        Аргументы:
        name (str): Название блюда.
        category (str): Категория блюда.
        weight (int): Вес блюда.
        cost (int): Стоимость блюда.
        """
        self.name = name
        self.category = category
        self.weight = weight
        self.cost = cost

    def __str__(self):
        """
        Возвращает строковое представление блюда для отображения.

        Возвращает:
        str: Строка с информацией о блюде.
        """
        return 'Dish:\n{} {}\nВес: {}\nЦена: {} рублей\n'.format(self.name, self.category, self.weight, self.cost)

    def __repr__(self):
        """
        Возвращает строковое представление блюда для разработчиков.

        Возвращает:
        str: Строка с подробной информацией о блюде.
        """
        return 'Dish(name="{}", category="{}", weight={}, cost={})'.format(self.name, self.category, self.weight, self.cost)

    def set_Dish(self, name, category, weight, cost):
        """
        Устанавливает параметры блюда.

        Аргументы:
        name (str): Название блюда.
        category (str): Категория блюда.
        weight (int): Вес блюда.
        cost (int): Стоимость блюда.
        """
        self.name = name
        self.category = category
        self.weight = int(weight)
        self.cost = int(cost)
    
    def get_Dish(self):
        """
        Возвращает информацию о блюде в виде строки.

        Возвращает:
        str: Строка с информацией о блюде.
        """
        return '{} {}\nВес: {}\nЦена: {} рублей\n'.format(self.name, self.category, self.weight, self.cost)

class Grup:
    """
    Класс для управления группой блюд.

    Содержит список блюд и словарь для быстрого доступа к блюдам по имени.
    """

    def __init__(self):
        """
        Инициализация экземпляра класса Grup.

        Создает пустой список блюд и пустой словарь.
        """
        self.A = []
        self.menu_dict = {}
        self.count = 0
    
    def __str__(self):
        """
        Возвращает строковое представление всех блюд в группе.

        Возвращает:
        str: Строка с информацией о всех блюдах.
        """
        s = ''
        i = 1
        for x in self.A:
            s += 'Dish:{}\n'.format(i)
            s += x.get_Dish()
            s += "\n"
            i += 1
        return s

    def read_data(self, file_name):
        """
        Читает данные из файла и добавляет блюда в группу.

        Аргументы:
        file_name (str): Имя файла с данными блюд.
        """
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 4:
                    dish_name, category, weight, cost = parts
                    dish = Dish()
                    dish.set_Dish(dish_name, category, weight, cost)
                    self.A.append(dish)
                    self.menu_dict[dish_name] = dish
        print("Data loaded: ", self.menu_dict)  # Отладочное сообщение

    def append_dish(self, name, category, weight, cost):
        """
        Добавляет новое блюдо в группу.

        Аргументы:
        name (str): Название блюда.
        category (str): Категория блюда.
        weight (int): Вес блюда.
        cost (int): Стоимость блюда.

        Возвращает:
        bool: True, если добавление прошло успешно, иначе False.
        """
        if not name or not category or not weight or not cost:
            return False

        try:
            weight = int(weight)
            cost = int(cost)
        except ValueError:
            return False

        new_dish = Dish(name, category, weight, cost)
        self.A.append(new_dish)
        self.menu_dict[name] = new_dish
        return True
    
    def delete_dish_by_name(self, name):
        """
        Удаляет блюдо по имени.

        Аргументы:
        name (str): Название блюда.

        Возвращает:
        bool: True, если удаление прошло успешно, иначе False.
        """
        if name in self.menu_dict:
            dish = self.menu_dict.pop(name)
            self.A.remove(dish)
            return True
        return False

    def delete_cell(self, row, col):
        """
        Удаляет содержимое ячейки по заданным координатам.

        Аргументы:
        row (int): Номер строки.
        col (int): Номер колонки.

        Возвращает:
        bool: True, если удаление прошло успешно, иначе False.
        """
        if row < len(self.A):
            dish = self.A[row]
            if col == 0:
                self.delete_dish_by_name(dish.name)
            elif col == 1:
                dish.category = ""
            elif col == 2:
                dish.weight = 0
            elif col == 3:
                dish.cost = 0
            return True
        return False

    def edit_cell(self, row, col, new_value):
        """
        Редактирует содержимое ячейки по заданным координатам и новому значению.

        Аргументы:
        row (int): Номер строки.
        col (int): Номер колонки.
        new_value (str): Новое значение.

        Возвращает:
        bool: True, если редактирование прошло успешно, иначе False.
        """
        if row < len(self.A):
            dish = self.A[row]
            if col == 0:
                self.delete_dish_by_name(dish.name)
                dish.name = new_value
                self.menu_dict[new_value] = dish
            elif col == 1:
                dish.category = new_value
            elif col == 2:
                dish.weight = int(new_value)
            elif col == 3:
                dish.cost = int(new_value)
            return True
        return False
