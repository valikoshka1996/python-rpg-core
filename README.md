### 📌 **README.md for `rpgcore.py`**  

```md
# RPGCore Library

RPGCore is a Python library designed to provide core mechanics for role-playing games (RPGs). It includes classes for characters, enemies, quests, locations, items, and races. Developers can use it to build text-based or graphical RPGs.

## 📥 Installation
No installation is required. Simply include `rpgcore.py` in your project directory and import it:

```python
import rpgcore
```

---

## 🚀 Features
- **Character Creation**: Define player stats, class, race, and inventory.
- **Quests System**: Assign, track, and complete quests.
- **Combat Mechanics**: Battle enemies with attack and damage calculations.
- **Inventory Management**: Equip weapons, armor, and use consumables.
- **Locations & Exploration**: Move between different locations.
- **Experience & Leveling**: Gain XP, earn rewards, and level up.

---

## 🏗️ **Usage Guide**

### 1️⃣ **Creating an Enemy**
```python
goblin = rpgcore.Enemy("Goblin", health=30, power=10)
print(goblin.get_name())  # Goblin
```

### 2️⃣ **Creating a Character**
```python
hero = rpgcore.Character("Hero", health=100, power=15, armor=5, money=50, race="Human", class_type="Warrior")
print(hero.get_info())
```

### 3️⃣ **Creating and Completing a Quest**
```python
quest = rpgcore.Quest("Hunt the Goblin", "Defeat a goblin in battle", salary=100, xp=50, rules={"kill_monster": ["Goblin"]})
hero.add_active_quest(quest)

# Simulating battle
goblin.set_damage(30)  # Killing the goblin
quest.add_killed_monster(goblin)

if quest.is_complete():
    hero.add_completed_quest(quest)
    print("Quest completed!")
```

### 4️⃣ **Moving Between Locations**
```python
hero.move_to("Forest")
print(hero.get_position())  # Forest
```

### 5️⃣ **Creating and Equipping Items**
```python
sword = rpgcore.Items("Iron Sword", item_type="weapon", power=20, cost=100)
hero.add_item(sword)
hero.equip_weapon(sword)
print(hero.get_weapon().get_name())  # Iron Sword
```

---

## 📜 **Class Reference**

### 🎭 **Character**
| Method | Description |
|--------|------------|
| `get_name()` | Returns character's name. |
| `get_health()` | Returns health points. |
| `get_power()` | Returns attack power. |
| `get_position()` | Returns current location. |
| `move_to(location)` | Moves character to a new location. |
| `attack()` | Performs an attack with randomized damage. |
| `take_damage(damage)` | Reduces health considering armor protection. |
| `add_item(item)` | Adds an item to inventory. |
| `equip_weapon(weapon)` | Equips a weapon. |
| `get_weapon()` | Returns equipped weapon. |
| `add_active_quest(quest)` | Assigns a quest to the character. |
| `add_completed_quest(quest)` | Marks a quest as completed and gives rewards. |

### 🛡️ **Enemy**
| Method | Description |
|--------|------------|
| `attack()` | Returns a random attack value. |
| `get_name()` | Returns enemy's name. |
| `get_health()` | Returns remaining health. |
| `is_dead()` | Checks if the enemy is dead. |
| `set_damage(damage)` | Reduces health by damage received. |

### 📜 **Quest**
| Method | Description |
|--------|------------|
| `get_actual_rules()` | Returns the quest's completion conditions. |
| `add_killed_monster(monster)` | Adds a defeated monster towards completion. |
| `add_visited_location(location)` | Marks a location as visited. |
| `add_collected_item(item)` | Marks an item as collected. |
| `is_complete()` | Checks if the quest is completed. |
| `complete_quest()` | Marks the quest as completed and returns rewards. |

### 🗺️ **Locations**
| Method | Description |
|--------|------------|
| `get_locations()` | Returns available locations. |
| `is_valid_location(location)` | Checks if a location is valid. |
| `add_location(location)` | Adds a new location. |

### 🎭 **Items**
| Method | Description |
|--------|------------|
| `get_name()` | Returns item name. |
| `get_power()` | Returns attack power (for weapons). |
| `get_armor()` | Returns armor value (for clothing). |
| `get_cost()` | Returns item cost. |

---

## 🔍 **Unit Testing**
To ensure everything is working correctly, run the unit tests:
```sh
python -m unittest test_rpgcore.py
```

---

## 🎮 **License**
This library is open-source. Feel free to modify and use it in your own RPG projects.

---

## 💡 **Future Improvements**
- Implement magic spells and skills.
- Add multiplayer interactions.
- Expand quest types with more conditions.

---

Happy coding! 🚀
