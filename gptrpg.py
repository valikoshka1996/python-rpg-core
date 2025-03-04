import random
import rpgcore

def create_character():
    print("Ласкаво просимо у світ пригод!")
    
    name = input("Введіть ім'я персонажа: ")
    
    # Вибір раси
    print("\nОберіть расу:")
    races = rpgcore.Race.get_races()
    for i, race in enumerate(races, 1):
        print(f"{i}. {race}")
    
    race_choice = int(input("Введіть номер раси: ")) - 1
    race = races[race_choice]
    
    # Вибір класу
    print("\nОберіть клас:")
    classes = rpgcore.ClassType.get_types()
    for i, c in enumerate(classes, 1):
        print(f"{i}. {c}")

    class_choice = int(input("Введіть номер класу: ")) - 1
    class_type = classes[class_choice]

    # Ініціалізація персонажа
    char = rpgcore.Character(name, 100, 10, 5, 50, race, class_type)
    
    print("\nПерсонаж створений!")
    print(char.get_info())
    
    return char

def get_random_quest():
    """Генерує випадковий квест"""
    quest_types = [
        ("Полювання на монстра", "kill_monster", ["Гоблін"]),
        ("Відвідування локації", "visited_location", ["Forest"]),
        ("Пошук предмета", "collected_item", ["Зельє здоров'я"])
    ]
    title, rule, target = random.choice(quest_types)
    return rpgcore.Quest(title, f"Виконайте завдання: {title}", 100, 50, {rule: target})

def show_quests(player):
    """Перегляд активних квестів"""
    print("\nВаші активні квести:")
    quests = player.get_active_quests()
    if quests:
        for i, q in enumerate(quests, 1):
            print(f"{i}. {q}")
    else:
        print("У вас немає активних квестів.")

def take_quest(player):
    """Додає випадковий квест"""
    quest = get_random_quest()
    player.add_active_quest(quest)
    print(f"\nВи взяли квест: {quest.name}")

def complete_quest(player):
    """Спроба завершити квест"""
    active_quests = [q for q in player.active_quests]  # Отримуємо список об'єктів Quest

    if not active_quests:
        print("\nУ вас немає активних квестів.")
        return

    print("\nВаші активні квести:")
    for i, quest in enumerate(active_quests, 1):
        print(f"{i}. {quest.name} - {quest.description}")

    choice = int(input("Виберіть квест для виконання: ")) - 1
    if choice < 0 or choice >= len(active_quests):
        print("Невірний вибір!")
        return

    quest = active_quests[choice]  # Отримуємо об'єкт `Quest`
    rules = quest.get_actual_rules()  # Отримуємо правила для виконання

    # Виконання різних типів квестів
    if "kill_monster" in rules:
        monster_name = rules["kill_monster"][0]  # Отримуємо конкретного монстра для квесту
        monster = rpgcore.Enemy(monster_name, 30, 10)  # Створюємо правильного ворога
        fight_monster(player, monster)  # Передаємо конкретного монстра в бій
        quest.add_killed_monster(monster)

    elif "visited_location" in rules:
        explore(player)
        quest.add_visited_location(rpgcore.Locations(player.get_position()))

    elif "collected_item" in rules:
        item_name = rules["collected_item"][0]
        item = rpgcore.Items(item_name, item_type="інше")  # Додаємо коректний тип предмета
        find_item(player)  # Симуляція знаходження предмета
        quest.add_collected_item(item)

    # Перевірка завершення квесту перед додаванням у виконані
    if not quest.is_complete():
        print(f"\n❌ Не виконані умови квесту: {quest.get_actual_rules()}")
        return

    player.add_completed_quest(quest)

    print("\n✅ Квест виконано! Ви отримали нагороду.")


def explore(player):
    """Подорож між локаціями"""
    print("\nОберіть місце для подорожі:")
    locations = rpgcore.Locations.get_locations()
    
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc}")

    choice = int(input("Введіть номер локації: ")) - 1
    new_location = locations[choice]

    player.move_to(new_location)
    print(f"Ви подорожували до {new_location}!")

def fight_monster(player, specific_monster=None):
    """Битва з випадковим монстром або конкретним (для квесту)"""
    if specific_monster:
        enemy = specific_monster  # Використовуємо монстра з квесту
    else:
        monsters = [
            rpgcore.Enemy("Гоблін", 30, 10),
            rpgcore.Enemy("Орк", 50, 15),
            rpgcore.Enemy("Дракон", 100, 30)
        ]
        enemy = random.choice(monsters)  # Випадковий монстр

    print(f"\nНа вас напав {enemy.get_name()}!")
    
    while not player.is_dead() and not enemy.is_dead():
        input("\nНатисніть Enter для атаки!")
        damage = player.attack()
        enemy.set_damage(damage)
        print(f"Ви завдали {damage} урону. У ворога залишилось {enemy.get_health()} HP.")

        if not enemy.is_dead():
            enemy_damage = enemy.attack()
            player.take_damage(enemy_damage)
            print(f"Ворог атакує! Ви отримали {enemy_damage} урону. У вас залишилось {player.get_health()} HP.")

    if player.is_dead():
        print("Вас переможено... Гра закінчена.")
        exit()
    else:
        print(f"Ви перемогли {enemy.get_name()}!")
        reward = random.randint(10, 50)
        player.gain_money(reward)
        print(f"Ви отримали {reward} монет!")

def find_item(player):
    """Отримання випадкового предмета"""
    items = [
        rpgcore.Items("Зельє здоров'я", item_type="ліки", health=20),
        rpgcore.Items("Меч", item_type="зброя", power=15, cost=100),
        rpgcore.Items("Щит", item_type="одяг", armor=10, cost=80)
    ]
    
    item = random.choice(items)
    player.add_item(item)
    print(f"Ви знайшли {item.get_name()}!")

def show_character_info(player):
    """Перегляд інформації про персонажа"""
    print("\nІнформація про персонажа:")
    info = player.get_info()
    for key, value in info.items():
        print(f"{key}: {value}")

def main_menu(player):
    """Головне меню гри"""
    while True:
        print("\n=== ГОЛОВНЕ МЕНЮ ===")
        print("1. Подорожувати")
        print("2. Переглянути інформацію про персонажа")
        print("3. Переглянути активні квести")
        print("4. Взяти новий квест")
        print("5. Виконати квест")
        print("6. Битися з монстром")
        print("7. Знайти предмет")
        print("8. Вийти з гри")
        
        choice = input("Оберіть дію: ")
        
        if choice == "1":
            explore(player)
        elif choice == "2":
            show_character_info(player)
        elif choice == "3":
            show_quests(player)
        elif choice == "4":
            take_quest(player)
        elif choice == "5":
            complete_quest(player)
        elif choice == "6":
            fight_monster(player)
        elif choice == "7":
            find_item(player)
        elif choice == "8":
            print("Гра завершена.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    player = create_character()
    main_menu(player)
