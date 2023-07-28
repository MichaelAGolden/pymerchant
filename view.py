from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import timedelta
from controller import Game
from tradeentity import Player

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.prompt import IntPrompt
from rich.table import Table


@dataclass
class View:
    """
    View component of the game, wraps around game object.

    This could be later replaced by a more complex system written in CURSES or some non-console based game.
    I've considered adding a GUI but that might be too much for this time
    """
    game: Game

    def __init__(self) -> None:
        """
        Initializes View object, defines menu and keyword attributes not set in @dataclass() init
        """
        self.game = Game()
        self.menu = ['Travel', 'Trade', 'Inventory',
                     'Wait (advance to next day)', 'Quit']
        self.menu_selection = None
        self.user_last_action = None
        self.time_passed = None
        self.user_selection = None
        self.console = Console()

    def game_loop(self):
        """
        Main loop that runs and draws the screen and calls the relevant functions in from view and game
        """
        while self.menu_selection != 'q':
            self.game.player.location.update_market(self.game.player.location)
            self.main_menu_view()
            self.process_input()

    # Menu selection methods
    def main_menu_view(self):
        """
        Displays game_menu and asks user for input

        """
        self.clear_sceen()
        self.get_game_status()

        print("What would you like to do?")

        for i, option in enumerate(self.menu):
            print(f"{i+1}. {option}")

        choice = self.get_input_for_range_val(self.menu)

        self.menu_selection = self.menu[choice - 1]

    def travel_view(self):
        self.clear_sceen()
        self.get_game_status()

        list_of_cities = self.get_sorted_cities()

        choice = self.get_input_for_range_val(list_of_cities)

        new_location = list_of_cities[choice - 1][0]

        self.time_passed = Player.get_time_to_travel(
            self.game.player, self.game.player.location, self.game.get_city(new_location))
        total_seconds = round(self.time_passed.total_seconds())

        for i in track(range(0, total_seconds), f"Traveling to {new_location.capitalize()}"):
            time.sleep(.00001)

        self.game.advance_days(self.time_passed)
        self.game.player.location = self.game.get_city(new_location)

        print(
            f"You have arrived in {self.game.player.location.name.capitalize()}.")

    def trade_view(self):
        self.clear_sceen()
        self.get_game_status()

        list_of_items = self.game.player.location.inv.get_list_of_items()

        self.build_item_table(list_of_items)

        choice = self.get_input_for_range_val(list_of_items, False)

        self.user_selection = list_of_items[choice - 1]

        # calc max amount player can purchase
        max_purchase_qty = round(
            self.game.player.inv.gold / self.user_selection.price)

        # validate they aren't buying more than the max otherwise prompt input over again
        user_input_qty = self.get_input_for_int_val(max_purchase_qty)

        # once qty selected subtract gold from player
        self.game.player.inv.gold -= user_input_qty * self.user_selection.price
        self.game.player.inv.get_player_item(
            self.user_selection.item_name).quantity += user_input_qty

        self.game.player.location.inv.get_market_item(
            self.user_selection.item_name).quantity -= user_input_qty

    def inventory_view(self):
        self.clear_sceen()
        self.get_game_status()
        table = Table.grid("Player Inventory")

        table.add_column("Trade Good", justify='right', no_wrap=True)
        table.add_column("Quantity", justify='left', no_wrap=True)
        table.add_column("Price", justify='right', no_wrap=True)
        table.add_column("Last Purchase Price", justify='right', no_wrap=True)
        table.add_column("Last Seen Price", justify='right', no_wrap=True)

        player_item_inventory = self.game.player.inv.get_list_of_items()
        for item in player_item_inventory:
            if item.quantity > 0:
                table.add_row(f"{item.item_name}",
                              f"{item.quantity}", f"{item.cost}")
        print(table)
        input("Press enter key to continue...")

    def wait(self):
        self.clear_sceen()
        self.get_game_status()

        # use timedelta to advance day by one
        next_day_datetime = (self.game.current_date +
                             timedelta(days=1))

        # use datetime.replace() function to set the date time to start of day when markets refresh
        next_day_datetime = next_day_datetime.replace(
            hour=6, minute=0, second=0)

        self.time_passed = next_day_datetime - self.game.current_date
        total_seconds = round(self.time_passed.total_seconds())
        for i in track(range(0, total_seconds), "Waiting till next day..."):
            time.sleep(.00001)
        self.game.advance_days(self.time_passed)

    def get_game_status(self):
        """
        Simple game status method intended to be called at start of each turn or menu selection

        Updated to use Rich for formatting
        """
        grid = Table.grid(expand=False)

        grid.add_column(justify="left")
        grid.add_row(f"Date: {self.game.current_date}")
        grid.add_row(
            f"Location: {self.game.player.location.name.capitalize()}")
        grid.add_row(f"Time Passed: {self.time_passed}")
        grid.add_row(f"Last Action: {self.user_last_action}")
        grid.add_row(f"Gold:  {self.game.player.inv.gold}")

        panel = Panel(grid)

        print(panel)

    def get_sorted_cities(self):
        """
        Returns list of cities sorted closest to furthest based on the city the player is in
        """
        city_distance_dict = self.game.player.location.sort_closest_cities(
        ).items()

        list_of_cities = []

        for i, (city, distance) in enumerate(city_distance_dict):
            print(f"{i+1}. {city.capitalize()} {distance} (distance in NM)")
            list_of_cities.append((city, distance))

        return list_of_cities

    @staticmethod
    def clear_sceen():
        """Function that clears screen depending on what OS user is running"""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def get_input_for_int_val(value, show_choices=False):
        range_of_menu = [str(num) for num in range(1, value + 1)]
        choice = IntPrompt.ask(
            f"Please choose the number coorresponding to your choice between 1 and {value}", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_input_for_range_val(value, show_choices=False):
        range_of_menu = [str(num) for num in range(1, len(value) + 1)]
        choice = IntPrompt.ask(
            f"Please enter a whole number between 1 and {len(value)}", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def build_item_table(list_of_items):
        table = Table()
        table.add_column("#")
        table.add_column("Trade Good")
        table.add_column("Stock")
        table.add_column("Price")
        for index, item in enumerate(list_of_items):
            table.add_row(
                f"{index+1}", f"{item.item_name.title()}", f"{item.quantity}", f"{item.price}")
        print(table)

    def process_input(self):
        if self.menu_selection == self.menu[0]:
            self.user_last_action = "Travel"
            self.travel_view()
        elif self.menu_selection == self.menu[1]:
            self.user_last_action = "Trade"
            self.trade_view()
        elif self.menu_selection == self.menu[2]:
            self.user_last_action = "Inventory"
            self.inventory_view()
        elif self.menu_selection == self.menu[3]:
            self.user_last_action = "Wait"
            self.wait()
        elif self.menu_selection == self.menu[4]:
            self.user_last_action = "q"
            print(self.user_last_action)
        else:
            print("Invalid input.")
