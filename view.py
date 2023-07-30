from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import timedelta, datetime
import random

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.prompt import IntPrompt
from rich.table import Table

from enumerations import CITIES, TRADING_HOUSE_DIALOGUE
from modifiers import MarketEvent
from tradeentity import City, Player
from inventory import MarketInv, PlayerInv


@dataclass()
class Game:
    """
    Game class holds all objects necessary for the game, including Player, City, and all of their objects and attriburtes

    Game logic and initialization of game occurs here
    """
    current_date = datetime(year=1323, month=7, day=29, hour=6, minute=0)
    player: Player

    def __init__(self) -> None:
        """
        Games

        Args:
            starting_city (str, optional): Name of starting_city player is located in. Defaults to 'lubeck'.
        """
        self.build_cities()
        self.update_city_inventories()
        self.player = self.create_player()

    def advance_days(self, time_to_advance: timedelta):
        """
        Advances game time by a datetime.timedelta

        Args:
            time (timedelta): timedelta is defined in datetime module
        """
        self.current_date += time_to_advance

    def build_cities(self) -> None:
        """
        Creates all city objects for game and assigns them to our game object

        To be run in __init__() function

        Note we use setattr() function because cities are not defined as keyword properties at time of
        """
        for city in CITIES.keys():
            new_city = City(city, travel_mod_list=list())
            setattr(self, city, new_city)

    def create_player(self) -> Player:
        """
        Creates player object for game

        Returns:
            Player: Player object
        """
        city = self.get_city('lubeck')
        return Player(city, travel_mod_list=[])

    def list_of_cities(self):
        """
        Returns list of cities in game

        Returns:
            List[City]: List of City objects in game
        """
        return [city for city in dir(self) if isinstance(getattr(self, city), City)]

    def get_city(self, city: str) -> City:
        """
        Returns city by str lookup

        Args:
            city (str): Name of city, not the City object itself

        Returns:
            City: City Object
        """
        return getattr(self, city)

    @staticmethod
    def update_market(city):
        """
        Updates all prices for items in a given city

        Args:
            city (City): City we are updating
        """
        city.inv.update_item_pricing()
        city.inv.update_item_quantity()

    def update_city_inventories(self) -> None:
        """
        Function to update inventory supply level and pricing for all cities in the game, to be run ONLY once per game day
        """
        # for city in self.list_of_cities():
        #     Economy.update_supply(city)
        #     Economy.update_demand(city)
        #     Economy.update_pricing(city)
        pass

    def check_MarketEvent(self, city: City):
        """
        Checks and resolves all MarketEvents in a given city, deleting any events at or beyond expiry

        Args:
            event (MarketEvent): The kMarketEvent to be deleted
        Calls:
            delete_MarketEvent(city)
        Returns:
            None
        """
        for event in MarketEvent.get_all_events(city):
            if event.time_to_expire <= self.current_date:
                MarketEvent.delete_MarketEvent(event)

    @staticmethod
    def execute_trade(item, quantity, player_inv: PlayerInv, market_inv: MarketInv, buying_or_selling):
        if buying_or_selling == 'buying':
            player_inv.get_player_item(item.item_name).quantity += quantity

            market_inv.get_market_item(item.item_name).quantity -= quantity

            player_inv.gold -= item.price * quantity
        elif buying_or_selling == 'selling':
            player_inv.get_player_item(item.item_name).quantity -= quantity

            market_inv.get_market_item(item.item_name).quantity += quantity

            player_inv.gold += item.price * quantity
        else:
            print("Error, no trade executed")


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
        Game.update_market(self.game.player.location)
        while self.menu_selection != 'q':
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

        choice = self.get_input_main_menu_selection(self.menu)

        self.menu_selection = self.menu[choice - 1]

    def travel_view(self):
        self.clear_sceen()
        self.get_game_status()

        list_of_cities = self.get_sorted_cities()

        choice = self.get_input_for_city_choice(list_of_cities)

        new_location = list_of_cities[choice - 1][0]

        self.time_passed = Player.get_time_to_travel(
            self.game.player, self.game.player.location, self.game.get_city(new_location))
        total_seconds = round(self.time_passed.total_seconds())

        for i in track(range(0, total_seconds), f"Traveling to {new_location.capitalize()}"):
            time.sleep(.00001)

        self.game.advance_days(self.time_passed)
        self.game.player.location = self.game.get_city(new_location)
        Game.update_market(self.game.player.location)
        print(
            f"You have arrived in {self.game.player.location.name.capitalize()}.")

    def trade_view(self):
        self.clear_sceen()
        self.get_game_status()

        # Get list of items in player city
        list_of_items = self.game.player.location.inv.get_list_of_items()

        # render table of items
        self.build_item_table(list_of_items)

        buying_or_selling = self.get_buy_sell_choice()

        # checks if trade valid for trade validation
        if buying_or_selling == 'buying':
            # get user input for list_of_items
            choice = self.get_input_for_item_selection(list_of_items, False)

            # set user_selection to MarketItem selected
            self.user_selection = list_of_items[choice]
            max_trade_qty = round(
                self.game.player.inv.gold / self.user_selection.price) if self.user_selection.price >= 0 else self.game.player.inv.gold
            user_input_qty = self.get_input_for_int_val(max_trade_qty)

            trade_valid = self.user_selection.check_buy(
                user_input_qty, self.game.player.inv.gold)

        elif buying_or_selling == 'selling':
            # get user input for list_of_items
            choice = self.get_input_for_item_selection(list_of_items, False)

            # set user_selection to MarketItem selected
            self.user_selection = list_of_items[choice]

            max_trade_qty = self.game.player.inv.get_player_item(
                self.user_selection.item_name).quantity

            if max_trade_qty == 0:
                print(
                    f"Looks like you don't have any {self.user_selection.item_name.capitalize()} to trade sir!")
                trade_valid = False

            else:
                user_input_qty = self.get_input_for_int_val(max_trade_qty)

                trade_valid = self.game.player.inv.get_player_item(
                    self.user_selection.item_name).check_sell(self.user_selection.quantity)

        elif buying_or_selling == 'return':
            trade_valid = False
        else:
            trade_valid = False

        if trade_valid:
            self.game.execute_trade(self.user_selection, max_trade_qty,
                                    self.game.player.inv, self.game.player.location.inv, buying_or_selling)
            input("Trade Complete, press enter to return to docks")
        else:
            input("Press enter to return to docks")

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
        Game.update_market(self.game.player.location)

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

    def get_input_main_menu_selection(self, value, show_choices=False):
        range_of_menu = [str(num) for num in range(1, len(value) + 1)]
        choice = IntPrompt.ask(
            f"Welcome to the city of {self.game.player.location.name.capitalize()}!\n(Enter a number between 1 and {len(value)}) ", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_input_for_city_choice(value, show_choices=False):
        range_of_menu = [str(num) for num in range(1, len(value) + 1)]
        choice = IntPrompt.ask(
            f"Where are we sailing to my lord?\n(Enter a number between 1 and {len(value)}) ", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_input_for_item_selection(value, show_choices=False):
        range_of_menu = [str(num) for num in range(1, len(value) + 1)]
        dialogue = random.choice(TRADING_HOUSE_DIALOGUE)
        choice = IntPrompt.ask(
            f"{dialogue}\n(Please enter a whole number between 1 and {len(value)})", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_buy_sell_choice():
        options = ['buying', 'selling', 'exit']
        range_of_menu = [str(num) for num in range(1, len(options) + 1)]
        choice = IntPrompt.ask(
            f"Please select from the following\n[1] Buy\n[2] Sell\n[3] Return to Menu\n ", choices=range_of_menu, show_choices=True)
        return options[choice - 1]

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
