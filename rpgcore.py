import random  # Імпортуємо модуль для генерації випадкових чисел

class Enemy:
    # Конструктор класу Enemy для ініціалізації імені, здоров'я та сили
    def __init__(self, name, health, power):
        self.name = name  # Ім'я ворога
        self.health = health  # Здоров'я ворога
        self.power = power  # Сила ворога

    # Метод для атаки ворога, випадково вибираємо силу атаки
    def attack(self):
        return random.randint(0, self.power)  # Вибір випадкового числа від 0 до power


    def get_power(self):
        return self.power
    # Отримання імені ворога
    def get_name(self):
        return self.name

    # Отримання здоров'я ворога
    def get_health(self):
        return self.health

    # Перевірка, чи мертвий ворог
    def is_dead(self):
        if self.health > 0:
            return False  # Якщо здоров'я більше за 0, ворог живий
        else:
            return True  # Якщо здоров'я <= 0, ворог мертвий

    # Встановлення пошкоджень ворогу
    def set_damage(self, damage):
        self.health -= damage  # Віднімаємо завдане пошкодження від здоров'я ворога

class Quest:
    is_complete = False
    rules_list = {
            "kill_monster": "check_monster_killed",  # Умова на вбивство монстра
            "visited_location": "check_location_visited",  # Умова на відвідування локації
            "collected_item": "check_item_collected",  # Умова на зібрання предмету
            "gather_resource": "check_resource_collected"  # Умова на збір ресурсу
        }
    # Конструктор класу Quest для ініціалізації квесту з атрибутами
    def __init__(self, name, description, salary, xp, rules):
        self.rules = {}
        self.name = name  # Назва квесту
        self.description = description  # Опис квесту
        self.salary = salary  # Нагорода за квест
        self.xp = xp  # Досвід за виконання квесту
        self.status = False  # Статус виконання квесту (не виконано за замовчуванням)
        self.set_rules(rules)  # Умови для виконання квесту

        # Списки для відстеження виконаних умов
        self.killed_monsters = []
        self.visited_locations = []
        self.collected_items = []
        self.collected_resources = []  # Зібрані ресурси (наприклад, дерево, камінь)


    def set_rules(self, rules):
        for rule in rules:
            if rule not in self.condition_methods():
                return "Правило:", rule, "не було додане так як воно недоступне. Доступні правила: ", self.condition_methods()
            else:
                self.rules[rule] = rules[rule]
        return self.rules

    def get_actual_rules(self):
        return self.rules
    
    def condition_methods(self):
        return self.rules_list
        

    # Додавання вбитого монстра до списку
    def add_killed_monster(self, monster):
        if not isinstance(monster, Enemy):
            raise ValueError("Monster isn't object of class Enemy")
        if monster.get_name() not in self.rules['kill_monster']:
            return "There are no mosters for this quest"
        elif monster.get_name() in self.rules['kill_monster']:
            if not monster.is_dead():
                return "Ворог ще живий"
            elif monster.is_dead():
                self.killed_monsters.append(monster.get_name())
                self.update_quest()

    def add_visited_location(self, location):
        if not isinstance(location, Locations):
            raise ValueError("location isn't object of class Locations")
        if location.get_current_location() not in self.get_actual_rules()['visited_location']:
            raise ValueError(f"Tere is no location for this quest")
        if location.get_current_location() in self.get_actual_rules()['visited_location']:
            self.visited_locations.append(location.get_current_location())
            self.update_quest()
            return self.visited_locations

    def add_collected_item(self, item):
        if not isinstance(item, Items):
            raise ValueError("item isn't object of class Items")
        if item.get_name() not in self.get_actual_rules()['collected_item']:
            raise ValueError(f"Tere is no item for this quest")
        if item.get_name() in self.get_actual_rules()['collected_item']:
            self.collected_items.append(item.get_name())
            self.update_quest()
        return self.collected_items

    def complete_quest(self):
        quest_items = {'xp': '', 'salary': ''}
        if self.get_actual_rules():
            print("Не виконані умови квесту:", self.get_actual_rules())
            return quest_items
        elif not self.get_actual_rules():
            self.is_complete = True
            if self.get_xp():
                quest_items['xp'] = self.get_xp()
            if self.get_salary():
                quest_items['salary'] = self.get_salary()
            return quest_items

    def is_complete(self):
        return self.is_complete

    def update_quest(self):
        active_quests = self.get_actual_rules()
        to_delete = []  # Список для запису елементів, які треба видалити
        for rule in active_quests:
            if rule == 'kill_monster':
                if active_quests[rule] in self.killed_monsters:
                    to_delete.append(rule)
            elif rule == 'visited_location':
                if active_quests[rule] in self.visited_locations:
                    to_delete.append(rule)
            elif rule == 'collected_item':
                if active_quests[rule] in self.collected_items:
                    to_delete.append(rule)
            elif rule == 'gather_resource':
                if active_quests[rule] in self.collected_resources:
                    to_delete.append(rule)
            else:
                return "Invalid rule"
        
        # Видаляємо елементи з self.rules після перебору
        for rule in to_delete:
        	del self.rules[rule]    	

    def get_salary(self):
        return self.salary

    def get_xp(self):
        return self.xp

    # Отримання списку вбитих монстрів
    def get_killed_monsters(self):
        return self.killed_monsters

    # Отримання списку відвіданих локацій
    def get_visited_locations(self):
        return self.visited_locations

    # Отримання списку зібраних предметів
    def get_collected_items(self):
        return self.collected_items

    # Отримання списку зібраних ресурсів
    def get_collected_resources(self):
        return self.collected_resources

# Клас Locations для роботи з локаціями
class Locations:
    locations = ['Capital', 'Forest', 'Cave', 'City', 'Sea', 'Mountain']
    
    def __init__(self, location):
        if location not in self.locations:
            raise ValueError(f"Wrong location. Actual: {self.locations}")
        self.location = location


    def get_current_location(self):
        return self.location

    @staticmethod
    # Отримання списку локацій
    def get_locations():
        return Locations.locations

    @staticmethod
    # Перевірка, чи є валідною локація
    def is_valid_location(position):
        return position in Locations.locations

    @staticmethod
    # Додавання нової локації
    def add_location(location):
        if location in Locations.locations:
            print("Локація вже вказана")
        else:
            Locations.locations.append(location)

# Клас для типів персонажів
class ClassType:
    class_types = ['Воїн', 'Паладін', 'Крадій', 'Маг']

    @staticmethod
    # Перевірка, чи є валідним тип класу
    def is_valid_type(type):
        return type in ClassType.class_types

    @staticmethod
    # Додавання нового типу класу
    def add_new_type(type):
        if type not in ClassType.class_types:
            ClassType.class_types.append(type)

    def __init__(self, health=0, power=0, type=None, position="Capital"):
        # Перевірка типу класу та локації
        if type and not ClassType.is_valid_type(type):
            ClassType.add_new_type(type)

        if type and not ClassType.is_valid_type(type):
            raise ValueError(f"Не правильний тип: {type}. Доступні типи: {', '.join(ClassType.class_types)}. ")

        # Приклад перевірки для локації (незважаючи на те, що Locations не визначений у вашому коді)
        if not Locations.is_valid_location(position):
            raise ValueError(f"Не правильна позиція: {position}. Доступні позиції: {', '.join(Locations.get_locations())}. ")

        self.health = health
        self.type = type if type else ClassType.class_types[0]
        self.power = power
        self.position = position
    @classmethod
    def get_health(self):
        return ClassType.health
    @classmethod
    def get_power(self):
        return ClassType.power
    @classmethod
    def get_class(self):
        return ClassType.type
    @classmethod
    def get_position(self):
        return ClassType.position

    @classmethod
    def create_character(cls, type, health, power, position):
        # Перевірка, чи існує тип у класах, якщо ні — додавання нового
        if not ClassType.is_valid_type(type):
            ClassType.add_new_type(type)
        return cls(health=health, power=power, type=type, position=position)

    @staticmethod
    def init_character(type):
        if not ClassType.is_valid_type(type):
            return "Wrong type. Avaliable types:", ClassType.get_types()
        elif type == 'Воїн':
            ClassType.health = 150
            ClassType.type = 'Воїн'
            ClassType.power = 200
            ClassType.position = 'City'
        elif type == 'Паладін':
            ClassType.health = 170
            ClassType.type = 'Воїн'
            ClassType.power = 180
            ClassType.position = 'Capital'
        elif type == 'Крадій':
            ClassType.health = 100
            ClassType.type = 'Воїн'
            ClassType.power = 150
            ClassType.position = 'Forest'
        elif type == 'Маг':
            ClassType.health = 200
            ClassType.type = 'Sea'
            ClassType.power = 200
            ClassType.position = 'City'

    @staticmethod
    # Отримання доступних типів класів
    def get_types():
        return ClassType.class_types



# Клас Items для роботи з предметами
class Items:
    def __init__(self, name, class_type=None, armor=0, power=0, cost=0, health=0, item_type="Інше"):
        valid_types = ClassType.get_types()  # Доступні типи класів
        item_types = ("одяг", "зброя", "ліки", "інше")  # Доступні типи предметів
        self.health = health
        
        # Перевірка валідності типу класу для предмета
        if class_type:
            if isinstance(class_type, list):
                invalid_types = [ct for ct in class_type if ct not in valid_types]
                if invalid_types:
                    raise ValueError(f"Не правильні типи: {', '.join(invalid_types)}. Доступні типи: {', '.join(valid_types)}.")
            elif class_type not in valid_types:
                raise ValueError(f"Не правильний тип: {class_type}. Доступні типи: {', '.join(valid_types)}.")
        
        self.name = name
        if item_type not in item_types:  # Перевірка типу предмета
            raise ValueError(f"Неправильний тип. Доступні типи: {item_types}")
        else:
            self.item_type = item_type

        self.class_type = class_type if class_type else [valid_types[0]]
        self.armor = armor
        self.power = power
        self.cost = cost

    # Отримання імені предмета
    def get_name(self):
        return self.name

    # Отримання типів класів, для яких підходить предмет
    def get_class_types(self):
        return self.class_type

    # Отримання рівня захисту
    def get_armor(self):
        return self.armor

    # Отримання сили предмета
    def get_power(self):
        return self.power

    # Отримання вартості предмета
    def get_cost(self):
        return self.cost

# Клас Race для роботи з расами персонажів
class Race:
    race_types = ["Людина", "Ельф", "Гном"]
    race = ''
    start_items = []
    health = 0

    def __init__(self, type, health, start_items):
        if type and not type in self.race_types:
            self.race_types.append(type)
        elif not type:
            raise ValueError(f"Не вказана раса")
        self.race = type
        self.health = health
        if isinstance(start_items, list):
            if not all(isinstance(item, Items) for item in start_items):
                raise ValueError("Кожен елемент в start_items має бути об'єктом класу Items")
        elif not isinstance(start_items, Items):
            raise ValueError("start_items має бути або об'єктом класу Items, або списком об'єктів класу Items")

        self.start_items.append(start_items)

    # Отримання доступних рас
    @staticmethod
    def get_races():
        return Race.race_types

    def get_race(self):
        return self.race

    @staticmethod
    def init_race(race):
        if race not in Race.race_types:
            raise ValueError("Invalid race. Avaliable races:", Race.race_types)
        else:
            Race.race = race
            if race == "Людина":
                Race.health = 10
            if race == "Ельф":
                Race.health = 20
            if race == "Гном":
                Race.health = 15


    # Отримання здоров'я раси
    @staticmethod
    def get_health():
        return Race.health

    # Отримання стартових предметів раси
    def get_start_items(self):
        for item in self.start_items:
            return item

class Character:
    position = ''
    race = ''
    class_type = ''
    def __init__(self, name, health, power, armor, money, race, class_type, bag_size=10, description="", level=1, experience=0):
        # Основні атрибути персонажа
        self.name = name
        self.health = health
        self.power = power
        self.armor = armor
        self.money = money
        self.set_race(race)  # Раса персонажа
        self.set_class(class_type)  # Клас персонажа
        self.bag_size = bag_size  # Розмір сумки
        self.description = description  # Опис персонажа
        self.level = level  # Рівень персонажа
        self.experience = experience  # Досвід персонажа

        # Статуси квестів
        self.active_quests = []  # Список активних квестів
        self.completed_quests = []  # Список виконаних квестів

        # Списки для предметів
        self.items = []  # Загальний список предметів
        self.clothing_hand = None  # Одяг на руки
        self.clothing_legs = None  # Одяг на ноги
        self.clothing_head = None  # Одяг на голову
        self.weapon = None  # Зброя


    def get_info(self):
        info = {}
        info['Name'] = self.name
        info['health'] = self.get_health()
        info['power'] = self.get_power()
        info['race'] = self.get_race()
        info['money'] = self.get_money()
        info['position'] = self.get_position()
        info['class'] = self.get_class()
        info['level'] = self.get_level()
        info['xp'] = self.get_experience()
        return info

    # Метод для отримання імені персонажа
    def get_name(self):
        return self.name

    def set_race(self, race):
        if self.race:
            return "Cannot change race"
        else:
            if race not in Race.get_races():
                return "Wrong race, avaliable races:", Race.get_races()
            else:
                self.race = race
                Race.init_race(race)
                self.health += Race.get_health()
        return self.race


    def set_class(self, class_type):
        if self.class_type:
            return "Cannot change class"
        else:
            if class_type not in ClassType.get_types():
                return "Wrong class type, avaliable types:", ClassType.get_types()
            else:
                self.class_type = class_type
                ClassType.init_character(type=class_type)
                self.health += ClassType.get_health()
                self.power += ClassType.get_power()
                self.move_to(ClassType.get_position())
        return self.class_type



    # Метод для отримання здоров'я персонажа
    def get_health(self):
        return self.health

    # Метод для отримання сили персонажа
    def get_power(self):
        return self.power

    # Метод для отримання броні персонажа
    def get_armor(self):
        return self.armor

    # Метод для отримання грошей персонажа
    def get_money(self):
        return self.money

    # Метод для отримання позиції персонажа
    def get_position(self):
        return self.position

    # Метод для отримання раси персонажа
    def get_race(self):
        return self.race

    # Метод для отримання класу персонажа
    def get_class(self):
        return self.class_type

    # Метод для отримання рівня персонажа
    def get_level(self):
        return self.level

    # Метод для отримання досвіду персонажа
    def get_experience(self):
        return self.experience

    # Метод для додавання активного квесту
    def add_active_quest(self, quest):
        if not isinstance(quest, Quest):
            raise ValueError("This Quest isn't object of class Quest")
        if quest in self.completed_quests:
            raise ValueError(f"Цей квест уже виконано, не можна додавати як активний.")
        if quest not in self.active_quests:
            self.active_quests.append(quest)
        else:
            raise ValueError(f"Цей квест вже є активним.")

    # Метод для додавання виконаного квесту
    def add_completed_quest(self, quest):
        if not isinstance(quest, Quest):
            raise ValueError("This Quest isn't object of class Quest")
        quest_items = {}
        if quest not in self.completed_quests:
            if not quest.is_complete():
                return "Quest isn't complete"
            else:
                quest_items = quest.complete_quest()
                if quest_items['xp']:
                    self.gain_experience(quest_items['xp'])
                if quest_items['salary']:
                    self.gain_money(quest_items['salary'])


    # Метод для додавання предмета в інвентар
    def add_item(self, item):
        if not isinstance(item, Items):
            raise ValueError("This item isn't object of class Items")
        if len(self.items) < self.bag_size:
            self.items.append(item)
        else:
            raise ValueError("Сумка переповнена!")

    # Метод для визначення чи має персонаж певний предмет
    def has_item(self, item_name):
        return any(item.get_name() == item_name for item in self.items)

    def get_active_quests(self):
        if self.active_quests:
            questlist = []
            for quest in self.active_quests:
                questlist.append(quest.get_actual_rules())
            return questlist
        else:    
            return False


    # Метод для одягання предмета на певну частину тіла
    def wear_clothing(self, item):
        if item.get_item_type() == "одяг":
            if "руки" in item.get_name():
                self.clothing_hand = item
            elif "ноги" in item.get_name():
                self.clothing_legs = item
            elif "голова" in item.get_name():
                self.clothing_head = item
            else:
                raise ValueError(f"Невідомий тип одягу для {item.get_name()}")
        else:
            raise ValueError(f"Предмет {item.get_name()} не є одягом!")

    # Метод для оснастки персонажа зброєю
    def equip_weapon(self, weapon):
        if weapon.get_item_type() == "зброя":
            self.weapon = weapon
        else:
            raise ValueError(f"Предмет {weapon.get_name()} не є зброєю!")

    # Метод для отримання всіх предметів в інвентарі
    def get_items(self):
        return self.items

    # Метод для отримання одягу персонажа
    def get_clothing(self):
        return {
            "head": self.clothing_head,
            "hand": self.clothing_hand,
            "legs": self.clothing_legs,
        }

    # Метод для отримання зброї персонажа
    def get_weapon(self):
        return self.weapon

    # Метод для визначення, чи є персонаж мертвим
    def is_dead(self):
        return self.health <= 0

    # Метод для нанесення шкоди персонажу
    def take_damage(self, damage):
        damage_after_armor = max(0, damage - self.armor)  # Враховуємо броню
        self.health -= damage_after_armor
        if self.health < 0:
            self.health = 0  # Здоров'я не може бути менше за 0
    
    # Метод для нанесення шкоди персонажу
    def attack(self):
        return random.randint(0, self.power) # Здоров'я не може бути менше за 0


    # Метод для лікування персонажа
    def heal(self, health_points):
        self.health += health_points
        if self.health > 100:  # Максимальне здоров'я не більше 100
            self.health = 100

    # Метод для переміщення персонажа
    def move_to(self, new_position):
        if Locations.is_valid_location(new_position):
            self.position = new_position
        else:
            raise ValueError(f"Невірна локація: {new_position}")

    # Метод для підвищення рівня
    def level_up(self):
        if self.experience >= 100:  # Наприклад, 100 XP для підвищення рівня
            self.level += 1
            self.experience = 0  # Скидаємо досвід після підвищення рівня
            print(f"Вітаємо! Ви підвищили рівень до {self.level}!")
        else:
            raise ValueError(f"Неможливо підвищити рівень. Не вистачає досвіду.")
    def gain_money(self, money):
        self.money += money

    # Метод для додавання досвіду
    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()  # Перевірка на підвищення рівня після отримання досвіду


