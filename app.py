from typing import Dict, Type
import time
# Define the Market class


import os
import time


class Market:
    def __init__(self, name, connected_cities, market_type):
        self.name = name
        self.connected_cities = connected_cities
        self.market_type = market_type
        self.market_inventory = {}

    def __repr__(self):
        return str(f"[{self.name}, {self.connected_cities}, {self.market_type}]")

    def set_market_inventory(self, market_inventory):
        self.market_inventory = market_inventory

    def get_market_inventory(self):
        return self.market_inventory

    def get_item_info(self, item):
        return self.market_inventory


# Define the Player class
class Player:
    def __init__(self, name, gold, location: Type[Market]) -> None:
        self.name = name
        self.gold = gold
        self.location: Type[Market] = location
        self.inventory: Dict[str, int] = {}

    def __repr__(self):
        return str(f"[{self.name}, {self.gold}, {self.inventory}, {self.location}]")

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
        print(f"It is currently day {self.day_count}")

    def process_input(self, user_input):
        if user_input == "1":
            # Travel
            print(f"You are currently in {self.player.location}.")
            print("Where would you like to go?")
            for i, city in enumerate(self.player.location.connected_cities):
                print(f"{i+1}. {city.name}")
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
            self.player.location = self.player.location.connected_cities[choice-1]
            print(f"You have arrived in {Player.location.name}.")
        elif user_input == "2":
            # Trade
            print("You chose to trade.")
        else:
            print("Invalid input.")


# Define the trade goods dictionary
trade_goods = {
    "Copper Ore": 20,
    "Iron Ore": 15,
    "Gold Ore": 5,
    "Wool Cloth": 30,
    "Silk Cloth": 20,
    "Mageweave Cloth": 10,
    "Light Leather": 25,
    "Medium Leather": 20,
    "Heavy Leather": 15,
    "Linen Bandage": 40,
    "Wool Bandage": 30,
    "Silk Bandage": 20,
}


# Define the player
stormwind = Market(
    "Stormwind", ["Iron Forge", "Darnassus", "Exodar"], "Major City")
iron_forge = Market(
    "Iron Forge", ["Stormwind", "Exodar", "Darnassus"], "Major City")
darnassus = Market(
    "Darnassus", ["Stormwind", "Iron Forge", "Exodar"], "Major City")
exodar = Market(
    "Exodar", ["Iron Forge", "Darnassus", "Stormwind"], "Major City")


# set all the markets to have the same inventory
for city in [stormwind, iron_forge, darnassus, exodar]:
    city.set_market_inventory(trade_goods)

maventa = Player("Maventa", 1000, stormwind)

# run the game loop
game = Game(maventa)
game.game_loop()
