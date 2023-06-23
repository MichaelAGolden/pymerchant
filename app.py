from typing import Type
import time
import os


class Market:

    market_types = {
        "general_town": {
            "name": "General Town",
            "good_produced": ["wood", "stone", "iron", "grain", "wool", "leather"],
            "buildings": ["Town Hall", "Inn", "Blacksmith", "Stable", "Market"],
            "base_inventory": {"wood": 100, "stone": 100, "iron": 100, "grain": 100, "wool": 100, "leather": 100},
            "base_price": {"wood": 5, "stone": 20, "iron": 40, "grain": 3, "wool": 7, "leather": 10},
        }
    }

    ITEM_LIST = {
        "wood": {'name': "Wood", "weight_multiple": .5, "base_price": 5, "occurrence": "common", "base_quantity": 100},
        "stone": {'name': "Stone", "weight_multiple": 1.0, "base_price": 20, "occurrence": "common", "base_quantity": 100},
        "iron": {'name': "Iron", "weight_multiple": 0.8, "base_price": 40, "occurrence": "common", "base_quantity": 100},
        "grain": {'name': "Grain", "weight_multiple": 0.1, "base_price": 3, "occurrence": "common", "base_quantity": 100},
        "wool": {'name': "Wool", "weight_multiple": .6, "base_price": 7, "occurrence": "common", "base_quantity": 100},
        "leather": {'name': "Leather", "weight_multiple": .7, "base_price": 10, "occurrence": "common", "base_quantity": 100}
    }

    def __init__(self, name, connected_cities, market_type):
        self.name = name
        self.connected_cities = connected_cities
        self.market_type = self.market_types[market_type]
        self.market_inventory = self.market_type["base_inventory"]
        self.market_price = self.market_type["base_price"]
        self.market_buildings = self.market_type["buildings"]
        self.market_goods = self.market_type["good_produced"]

    def __repr__(self):
        return self.name

    def get_market_listings(self):
        table = list()
        for good, price in self.market_price.items():
            table.append([good, self.market_inventory[good], price])
        return table


class Player:
    location: Market

    def __init__(self, name, gold, location) -> None:
        self.name = name
        self.gold = gold
        self.location = location
        self.max_capacity: float = 300
        self.inventory = self.init_inventory()

    def __repr__(self):
        return str(f"[{self.name}, {self.gold}, {self.inventory}, {self.location.name}]")

    def init_inventory(self):
        items = self.location.ITEM_LIST
        return {k: {'quantity': 0, 'avg_cost': 0.0, 'last_purchase_price': 0.0, 'weight_multiple': v['weight_multiple']} for k, v in items.items()}

    def get_capacity(self):
        self.max_capacity
        self.load = sum([v['quantity'] * v['weight_multiple']
                        for v in self.inventory.values()])
        return self.max_capacity - self.load

    def update_inventory(self, item_name, quantity, price):
        self.inventory[item_name]['quantity'] += quantity
        self.inventory[item_name]['avg_cost'] = (
            self.inventory[item_name]['avg_cost'] + (quantity * price)) / ((self.inventory[item_name]['quantity']) + quantity)
        self.inventory[item_name]['last_purchase_price'] = price
        self.inventory[item_name]['weight_multiple'] = self.location.ITEM_LIST[item_name]['weight_multiple']


class Game:

    def __init__(self, player: Type[Player]) -> None:
        self.day_count = 1
        self.player = player
        self.menu = ["Travel", "Market", "Inventory", "Quit"]
        self.menu_selection = None
        self.user_last_action = None

    def game_loop(self):

        os.system('clear' if os.name == 'posix' else 'cls')
        while True:

            os.system('clear' if os.name == 'posix' else 'cls')
            self.print_game_status()

            self.game_menu()

            self.process_input()

            if self.menu_selection == self.menu[3]:
                break

            time.sleep(0.1)
            self.day_count += 1

    def print_game_status(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("Day:", self.day_count)
        print("Location:", self.player.location)
        print("Gold:", self.player.gold)
        print("Last Action:", self.user_last_action)

    def game_menu(self):
        print("What would you like to do?")
        for i, option in enumerate(self.menu):
            print(f"{i+1}. {option}")
        choice = input("Enter the number of your choice: ")
        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.menu):
                raise ValueError
        except ValueError:
            print(
                f"Invalid choice. Please enter a number between 1 and {len(self.menu)}.")
            return self.game_menu()
        self.menu_selection = self.menu[choice - 1]

    def travel(self, statement=None):
        # move to view controller
        self.print_game_status()

        if statement:
            print(statement)
        else:
            print("Where would you like to go?")

        for i, city in enumerate(self.player.location.connected_cities):
            print(f"{i+1}. {city}")
        choice = input(
            "Enter:")

        # Choice validation move to seperate files
        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.player.location.connected_cities):
                raise ValueError
        except ValueError:
            print(
                error := f"Invalid choice. Please enter a number between 1 and {len(self.player.location.connected_cities)}.")
            return self.travel(error)
        self.player.location = self.player.location.connected_cities[choice - 1]
        print(f"You have arrived in {self.player.location.name}.")

    def trade(self, statement=None):
        """_summary_

        Args:
            statement (_type_, optional): A message from try-except block for input and trade validation. Defaults to None.

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """

        # Move to some view controller
        self.print_game_status()

        # return exception from try-block,
        if statement:
            print(statement)
        item_list = self.player.location.get_market_listings()

        # Build table for displaying trade - refactor into a function
        for idx, item in enumerate(item_list):
            print(f"{idx}) {item[0]}: {item[1]} at {item[2]} gold each.")

        # Get User Input - refactor into other functions?
        user_item_choice = int(
            input("Enter the number cooresponding to the item: "))
        user_item_qty = int(input("How many would you like to buy? "))

        # Variable assignment
        item_price = item_list[user_item_choice][2]
        user_item_cost = user_item_qty * item_price
        user_item_name = item_list[user_item_choice - 1][0]

        # Validation Block - Refactor out of trade function
        # breakout f-strings into variables instead of walrus operator

        # Range of numbers validation
        try:
            if user_item_choice < 1 or user_item_choice > len(item_list):
                raise ValueError
        except ValueError:
            print(
                invalid_input := f"Invalid choice. Please enter a number between 1 and {len(item_list)}.")
            return self.trade(invalid_input)

        # Affordability Validation
        try:
            if user_item_cost > self.player.gold:
                raise ValueError
        except ValueError:
            print(not_enough_gold := "You don't have enough gold for that.")
            return self.trade(not_enough_gold)

        # Inventory Capacity Validation
        try:
            if user_item_qty > self.player.get_capacity():
                raise ValueError
        except ValueError:
            print(lack_of_space :=
                  "You don't have enough space in your inventory for that.")
            return self.trade(lack_of_space)

        # update gold/inventory
        self.player.gold -= user_item_cost
        self.player.update_inventory(
            user_item_name, user_item_qty, item_price)

    # Main Menu selection
    def process_input(self):
        if self.menu_selection == self.menu[0]:
            self.user_last_action = "Travel"
            self.travel()
        elif self.menu_selection == self.menu[1]:
            self.user_last_action = "Trade"
            self.trade()
        elif self.menu_selection == self.menu[2]:
            self.user_last_action = "Map"
            print(self.user_last_action)
        elif self.menu_selection == self.menu[3]:
            self.user_last_action = "Quit"
            print(self.user_last_action)
        else:
            print("Invalid input.")


# Initialize market objects - move to class - randomized at start
stormwind = Market("Stormwind", [], "general_town")
iron_forge = Market("Iron Forge", [], "general_town")
darnassus = Market("Darnassus", [], "general_town")
exodar = Market("Exodar", [], "general_town")

# Initialize market connected cities - move to a function in a class, need to make randomized at game start
stormwind.connected_cities = [iron_forge, darnassus, exodar]
iron_forge.connected_cities = [stormwind, exodar, darnassus]
darnassus.connected_cities = [stormwind, iron_forge, exodar]
exodar.connected_cities = [iron_forge, darnassus, stormwind]


# Move to class - customizable at start of game
maventa = Player("Maventa", 1000, stormwind)

# move game loop to seperate file
game = Game(maventa)
game.game_loop()
