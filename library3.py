class Dish:
    def __init__(self, name="", category="", weight=None, cost=None):
        self.name = name
        self.category = category
        self.weight = weight
        self.cost = cost

    def __str__(self):
        return 'Dish:\n{} {}\nВес: {}\nЦена: {} рублей\n'.format(self.name, self.category, self.weight, self.cost)

    def __repr__(self):
        return 'Dish(name="{}", category="{}", weight={}, cost={})'.format(self.name, self.category, self.weight, self.cost)

    def setDish(self, name, category, weight, cost):
        self.name = name
        self.category = category
        self.weight = int(weight)
        self.cost = int(cost)
    
    def getDish(self):
        return '{} {}\nВес: {}\nЦена: {} рублей\n'.format(self.name, self.category, self.weight, self.cost)

class Grup:
    def __init__(self):
        self.A = []
        self.menu_dict = {}
        self.count = 0
    
    def __str__(self):
        s = ''
        i = 1
        for x in self.A:
            s += 'Dish:{}\n'.format(i)
            s += x.getDish()
            s += "\n"
            i += 1
        return s

    def read_data(self, file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 4:
                    dish_name, category, weight, cost = parts
                    dish = Dish()
                    dish.setDish(dish_name, category, weight, cost)
                    self.A.append(dish)
                    self.menu_dict[dish_name] = dish
        print("Data loaded: ", self.menu_dict)  # Отладочное сообщение

    def append_dish(self, name, category, weight, cost):
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
        if name in self.menu_dict:
            dish = self.menu_dict.pop(name)
            self.A.remove(dish)
            return True
        return False

    def delete_cell(self, row, col):
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

# Функция для рекурсивного вывода данных блюд категории X в файл
def write_category_to_file(category, dishes, file):
    if not dishes:
        return
    dish_name, dish_data = dishes[0]
    if dish_data.category == category:
        file.write(f"{dish_data}\n")
    write_category_to_file(category, dishes[1:], file)

def write_category(category, menu_dict, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        write_category_to_file(category, list(menu_dict.items()), file)

# Функция для формирования списка L с данными о блюдах категории X, стоимостью не более Y рублей, отсортированным по стоимости
def filter_and_sort_dishes(category, max_price, menu_dict):
    filtered_dishes = [dish for dish in menu_dict.values() if dish.category == category and dish.cost <= max_price]

    # Пузырьковая сортировка списка по стоимости
    n = len(filtered_dishes)
    for i in range(n):
        for j in range(0, n-i-1):
            if filtered_dishes[j].cost > filtered_dishes[j+1].cost:
                filtered_dishes[j], filtered_dishes[j+1] = filtered_dishes[j+1], filtered_dishes[j]

    return filtered_dishes

# Функция для линейного поиска блюда в списке L
def linear_search(dish_name, dish_list):
    for dish in dish_list:
        if dish.name == dish_name:
            return dish
    return None

# Тестирование
if __name__ == "__main__":
    Gr = Grup()
    Gr.read_data("text.txt")
    print("Меню:", Gr.menu_dict)
    write_category("первые блюда", Gr.menu_dict, "output.txt")
    print("Категория 'первые блюда' записана в файл 'output.txt'.")
