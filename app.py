from typing import Dict, Type
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


class Player:
    location: Market

    def __init__(self, name, gold, location) -> None:
        self.name = name
        self.gold = gold
        self.location = location
        self.inventory: Dict[str, int] = {}

    def __repr__(self):
        return str(f"[{self.name}, {self.gold}, {self.inventory}, {self.location.name}]")


class Game:

    def __init__(self, player: Type[Player]) -> None:
        self.day_count = 1
        self.player = player
        self.menu = ["Travel", "Market", "Inventory", "Quit"]
        self.menu_selection = None
        self.user_last_action = None

    def game_loop(self):
        # Clear the screen
        os.system('clear' if os.name == 'posix' else 'cls')
        while True:
            # Update the screen (print whatever information the player needs to know)
            os.system('clear' if os.name == 'posix' else 'cls')
            self.print_game_status()

            self.game_menu()

            # Process user input (do whatever the game needs to do based on the input)
            self.process_input()
            # Break loop if the user wants to quit (you may want to handle this differently)
            if self.menu_selection == self.menu[3]:
                break
            # Optional: wait a short period before the next iteration
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

    def travel(self):
        self.print_game_status()
        print("Where would you like to go?")
        for i, city in enumerate(self.player.location.connected_cities):
            print(f"{i+1}. {city}")
        choice = input(
            "Enter:")
        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.player.location.connected_cities):
                raise ValueError
        except ValueError:
            print(
                f"Invalid choice. Please enter a number between 1 and {len(self.player.location.connected_cities)}.")
            return self.travel()
        self.player.location = self.player.location.connected_cities[choice - 1]
        print(f"You have arrived in {self.player.location.name}.")

    def trade(self):
        self.print_game_status()

    def process_input(self):
        if self.menu_selection == self.menu[0]:
            self.user_last_action = "Travel"
            self.travel()
        elif self.menu_selection == self.menu[1]:
            self.user_last_action = "Trade"
            print(self.user_last_action)
        elif self.menu_selection == self.menu[2]:
            self.user_last_action = "Map"
            print(self.user_last_action)
        elif self.menu_selection == self.menu[3]:
            self.user_last_action = "Quit"
            print(self.user_last_action)
        else:
            print("Invalid input.")


stormwind = Market("Stormwind", [], "general_town")
iron_forge = Market("Iron Forge", [], "general_town")
darnassus = Market("Darnassus", [], "general_town")
exodar = Market("Exodar", [], "general_town")

stormwind.connected_cities = [iron_forge, darnassus, exodar]
iron_forge.connected_cities = [stormwind, exodar, darnassus]
darnassus.connected_cities = [stormwind, iron_forge, exodar]
exodar.connected_cities = [iron_forge, darnassus, stormwind]


maventa = Player("Maventa", 1000, stormwind)


game = Game(maventa)
game.game_loop()
