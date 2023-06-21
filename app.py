from typing import Dict, Type
import time
import os


# Define the Market class
class Market:

    def __init__(self, name, connected_cities, market_type):
        self.name = name
        self.connected_cities = connected_cities
        self.market_type = market_type
        self.market_inventory = {}

    def __repr__(self):
        return self.name

    def set_market_inventory(self, market_inventory):
        self.market_inventory = market_inventory

    def get_market_inventory(self):
        return self.market_inventory

    def get_item_info(self, item):
        return self.market_inventory


# Define the Player class
class Player:
    location: Market

    def __init__(self, name, gold, location) -> None:
        self.name = name
        self.gold = gold
        self.location = location
        self.inventory: Dict[str, int] = {}

    def __repr__(self):
        return str(f"[{self.name}, {self.gold}, {self.inventory}, {self.location.name}]")

    def purchase(self, quantity, item, item_price, market):
        if item not in market.market_inventory or market.market_inventory[item] < quantity or self.gold < quantity * item_price:
            return False

        # Create a copy of the player's inventory and market's inventory
        player_inventory_copy = self.inventory.copy()
        market_inventory_copy = market.market_inventory.copy()

        # Update the copies with the proposed transfer
        player_inventory_copy[item] = player_inventory_copy.get(
            item, 0) + quantity
        market_inventory_copy[item] -= quantity

        # Check if the transfer is valid
        if any(v < 0 for v in market_inventory_copy.values()):
            return False

        # Update the actual player and market inventories
        self.inventory = player_inventory_copy
        market.market_inventory = market_inventory_copy

        # Deduct the gold from the player
        self.gold -= quantity * item_price

        return True


class Game:

    def __init__(self, player: Type[Player]) -> None:
        self.day_count = 1
        self.player = player

    def game_loop(self):
        # Clear the screen
        os.system('clear' if os.name == 'posix' else 'cls')
        while True:
            # Update the screen (print whatever information the player needs to know)
            os.system('clear' if os.name == 'posix' else 'cls')
            self.print_game_status()
            # Wait for user input
            user_input = input("What do you want to do? ")
            # Process user input (do whatever the game needs to do based on the input)
            self.process_input(user_input)
            # Break loop if the user wants to quit (you may want to handle this differently)
            if user_input.lower() == "quit":
                break
            # Optional: wait a short period before the next iteration
            time.sleep(0.1)
            self.day_count += 1

    def print_game_status(self):
        # Just a placeholder, replace this with your game logic
        print(f"It is currently day {self.day_count} and you are in {self.player.location.name}.")

    def process_input(self, user_input):
        if user_input == "1":
            # Travel
            print(f"You are currently in {self.player.location.name}.")
            print("Where would you like to go?")
            for i, city in enumerate(self.player.location.connected_cities):
                print(f"{i+1}. {city}")
            choice = input(
                "Enter the number of the city you would like to travel to: ")
            try:
                choice = int(choice)
                if choice < 1 or choice > len(self.player.location.connected_cities):
                    raise ValueError
            except ValueError:
                print(
                    f"Invalid choice. Please enter a number between 1 and {len(self.player.location.connected_cities)}.")
                return
            self.player.location = self.player.location.connected_cities[choice - 1]
            print(f"You have arrived in {self.player.location.name}.")
        elif user_input == "2":
            # Trade
            print("You chose to trade.")
        else:
            print("Invalid input.")


trade_goods = [
    {"name": "Iron Ore", "quantity": 50, "price": 300},
    {"name": "Timber", "quantity": 100, "price": 200},
    {"name": "Wool", "quantity": 80, "price": 100},
    {"name": "Grain", "quantity": 120, "price": 50},
    {"name": "Wine", "quantity": 60, "price": 400},
    {"name": "Cloth", "quantity": 30, "price": 500},
    {"name": "Salt", "quantity": 40, "price": 150},
    {"name": "Fish", "quantity": 70, "price": 100},
    {"name": "Cheese", "quantity": 90, "price": 250},
    {"name": "Beer", "quantity": 60, "price": 350},
]


stormwind = Market("Stormwind", [], "Major City")
iron_forge = Market("Iron Forge", [], "Major City")
darnassus = Market("Darnassus", [], "Major City")
exodar = Market("Exodar", [], "Major City")

stormwind.connected_cities = [iron_forge, darnassus, exodar]
iron_forge.connected_cities = [stormwind, exodar, darnassus]
darnassus.connected_cities = [stormwind, iron_forge, exodar]
exodar.connected_cities = [iron_forge, darnassus, stormwind]

for city in [stormwind, iron_forge, darnassus, exodar]:
    city.set_market_inventory(trade_goods)

maventa = Player("Maventa", 1000, stormwind)


game = Game(maventa)
game.game_loop()
