from __future__ import annotations
from typing import Type
from player import Player
import os
import time
from validators import Validators


class Game:

    def __init__(self, player: Type[Player]) -> None:
        self.day_count = 1
        self.player = player
        self.menu = ["Travel", "Trade", "Inventory", "Quit"]
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

            time.sleep(1.5)
            self.day_count += 1

    def print_game_status(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"Day: {self.day_count} Location: {self.player.location}")
        print("Last Action:", self.user_last_action)
        print(self.player.show_inventory())
        print("Gold:", self.player.gold)

    def game_menu(self, statement=None):
        if statement:
            print(statement)
        print("What would you like to do?")
        for i, option in enumerate(self.menu):
            print(f"{i+1}. {option}")
        choice = int(input("Enter the number of your choice: "))
        Validators.range_of_list(choice, self.menu, self.game_menu)
        self.menu_selection = self.menu[choice - 1]

    def travel(self, statement=None):
        """travel _summary_

        Args:
            statement (_type_, optional): _description_. Defaults to None.
        """

        self.print_game_status()
        if statement:
            print(statement)
        else:
            print("Pick your destination")

        for i, city in enumerate(self.player.location.connected_cities):
            print(f"{i+1}. {city}")
        choice = int(input(
            "Enter the number cooresponding with the location: "))
        Validators.range_of_list(
            choice, self.player.location.connected_cities, self.travel)

        self.player.location = self.player.location.connected_cities[choice - 1]
        print(self.player.location)
        print(f"You have arrived in {self.player.location}.")

    def trade(self, statement=None):
        """trade _summary_

        Args:
            statement (_type_, optional): _description_. Defaults to None.
        """
        self.print_game_status()
        if statement:
            print(statement)
        item_list = self.player.location.get_market_listings()

        # Build table for displaying trade - refactor into a function
        for idx, item in enumerate(item_list):
            print(
                f"{idx+1}) --{item[0]}--|-----{item[0][0]}-----|------{item[0][1]}-------")

        # Get User Input - refactor into other functions?
        user_item_choice = int(
            input("Enter the number cooresponding to the item: "))
        Validators.range_of_list(user_item_choice, item_list, self.trade)

        user_item_qty = int(input("How many would you like to buy? "))

        # Variable assignment
        item_price = item_list[user_item_choice][2]
        user_item_cost = user_item_qty * item_price
        user_item_name = item_list[user_item_choice - 1][0]

        Validators.affordability_check(user_item_cost, self.player, self.trade)
        Validators.check_inventory_capacity(
            user_item_qty, self.player, self.trade)

        self.player.buy_update_inventory(
            user_item_name, user_item_qty, item_price, user_item_cost)

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
