from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import timedelta, datetime
import random
from math import floor

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.prompt import IntPrompt
from rich.table import Table

from enumerations import CITIES, TRADING_HOUSE_DIALOGUE
from tradeentity import City, Player
from inventory import MarketInv, PlayerInv
from item import Transaction


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
        self.player = self.create_player()

    def advance_time(self, time_to_advance: timedelta):
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

    # def check_MarketEvent(self, city: City):
    #     """
    #     Checks and resolves all MarketEvents in a given city, deleting any events at or beyond expiry

    #     Args:
    #         event (MarketEvent): The kMarketEvent to be deleted
    #     Calls:
    #         delete_MarketEvent(city)
    #     Returns:
    #         None
    #     """
    #     for event in MarketEvent.get_all_events(city):
    #         if event.time_to_expire <= self.current_date:
    #             MarketEvent.delete_MarketEvent(event)

    def execute_trade(self, item, trade_quantity, player_inv: PlayerInv, market_inv: MarketInv, buying_or_selling):
        if buying_or_selling == 'buying':
            self.player.inv.get_player_item(
                item.item_name).quantity += trade_quantity

            item.quantity -= trade_quantity

            player_inv.gold -= item.price * trade_quantity

            # update the item cost for the PlayerItem in the PlayerInv
            player_inv.get_player_item(item.item_name).add_transaction(
                Transaction(price=item.price, quantity=trade_quantity, type_of_transaction='buy', date=self.current_date))

        elif buying_or_selling == 'selling':
            self.player.inv.get_player_item(
                item.item_name).quantity -= trade_quantity

            self.player.location.inv.get_market_item(
                item.item_name).quantity += trade_quantity

            player_inv.gold += item.price * trade_quantity

            player_inv.get_player_item(item.item_name).add_transaction(
                Transaction(price=item.price, quantity=trade_quantity, type_of_transaction='sell', date=self.current_date))

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
        self.title_screen()
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

        print(
            f"Welcome to the city of {self.game.player.location.name.capitalize()}!")
        print("What would you like to do?")

        for index, option in enumerate(self.menu):
            print(f"{index+1}. {option}")

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

        self.game.advance_time(self.time_passed)
        self.game.player.location = self.game.get_city(new_location)
        Game.update_market(self.game.player.location)
        print(
            f"You have arrived in {self.game.player.location.name.capitalize()}.")

    def trade_view(self):
        self.clear_sceen()
        self.get_game_status()

        # Get list of items in player city
        list_of_items = self.game.player.location.inv.get_list_of_items()
        player_list_of_items = self.game.player.inv.get_list_of_items()
        # render table of items

        table = self.build_combined_inventory_table(
            list_of_items, player_list_of_items)
        print(table)

        buying_or_selling = self.get_buy_sell_choice()

        # checks if trade valid for trade validation
        if buying_or_selling == 'buying':
            # get user input for list_of_items
            choice = self.get_input_for_item_selection(list_of_items, False)

            # set user_selection to MarketItem selected
            self.user_selection = list_of_items[choice - 1]
            # floor for max trade quantity taking into account what is available in the market quantity
            max_trade_qty = floor(
                self.game.player.inv.gold / self.user_selection.price)

            max_trade_qty = min(max_trade_qty, self.game.player.location.inv.get_market_item(
                self.user_selection.item_name).quantity)

            if max_trade_qty > 0:
                user_input_qty = self.get_input_for_qty_buy(
                    max_trade_qty, self.user_selection.item_name)

                trade_valid = self.user_selection.check_buy(
                    user_input_qty, self.game.player.inv.gold)

        elif buying_or_selling == 'selling':
            # get user input for list_of_items
            choice = self.get_input_for_item_selection(list_of_items, False)

            # set user_selection to MarketItem selected
            self.user_selection = list_of_items[choice - 1]

            max_trade_qty = self.game.player.inv.get_player_item(
                self.user_selection.item_name).quantity

            if max_trade_qty == 0:
                print(
                    f"Looks like you don't have any {self.user_selection.item_name} to trade sir!")
                trade_valid = False

            else:
                user_input_qty = self.get_input_for_qty_sell(
                    max_trade_qty, self.user_selection.item_name)

                player_item_to_check = self.game.player.inv.get_player_item(
                    self.user_selection.item_name)

                trade_valid = player_item_to_check.check_sell()

        elif buying_or_selling == 'return':
            trade_valid = False
        else:
            trade_valid = False

        if trade_valid:
            self.game.execute_trade(self.user_selection, user_input_qty,
                                    self.game.player.inv, self.game.player.location.inv, buying_or_selling)
            input("Trade Complete, press enter to return to docks")
        else:
            input("Press enter to return to docks")

    def inventory_view(self):
        self.clear_sceen()
        self.get_game_status()
        player_inventory_table = self.build_player_item_table(
            self.game.player.inv.get_list_of_items())

        print(player_inventory_table)

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
        self.game.advance_time(self.time_passed)
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
            f"Please choose the number coorresponding to your choice from 1 to {value}", choices=range_of_menu, show_choices=show_choices)
        return choice

    def get_input_main_menu_selection(self, value, show_choices=False):
        range_of_menu = [str(num) for num in range(1, len(value) + 1)]
        choice = IntPrompt.ask(
            f"(Enter a number from 1 to {len(value)}) ", choices=range_of_menu, show_choices=show_choices)
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
        choice = IntPrompt.ask(
            f"Please select an item from the tables above!\n(Please enter a number between 1 and {len(value)})", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_input_for_qty_buy(value, trade_good, show_choices=False):
        range_of_menu = [str(num) for num in range(1, value + 1)]
        dialogue = f"How much {trade_good} would you like to buy?"
        choice = IntPrompt.ask(
            f"{dialogue}\n(Please enter a whole number from 1 to {value})", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_input_for_qty_sell(value, trade_good, show_choices=False):
        range_of_menu = [str(num) for num in range(1, value + 1)]
        dialogue = f"How much {trade_good} would you like to sell?"
        choice = IntPrompt.ask(
            f"{dialogue}\n(Please enter a whole number from 1 to {value})", choices=range_of_menu, show_choices=show_choices)
        return choice

    @staticmethod
    def get_buy_sell_choice():
        options = ['buying', 'selling', 'exit']
        range_of_menu = [str(num) for num in range(1, len(options) + 1)]
        dialogue = random.choice(TRADING_HOUSE_DIALOGUE)
        print(dialogue)
        choice = IntPrompt.ask(
            "Please select from the following\n[1] Buy\n[2] Sell\n[3] Return to Menu\n ", choices=range_of_menu, show_choices=True)
        return options[choice - 1]

    @staticmethod
    def build_trading_item_table(list_of_items):
        table = Table(title="Trading House Inv")
        table.add_column("#")
        table.add_column("Trade Good")
        table.add_column("Stock")
        table.add_column("Price")
        for index, item in enumerate(list_of_items):
            table.add_row(
                f"{index+1}", f"{item.item_name.title()}", f"{item.quantity}", f"{item.price}")
        return table

    @staticmethod
    def build_player_item_table(list_of_items):
        table = Table(title="Cargo Hold Inv")
        table.add_column("#")
        table.add_column("Trade Good")
        table.add_column("Inventory")
        table.add_column("Cost")
        for index, item in enumerate(list_of_items):
            table.add_row(
                f"{index+1}", f"{item.item_name.title()}", f"{item.quantity}", f"{item.cost}")
        return table

    @staticmethod
    def build_combined_inventory_table(trading_house_items, cargo_hold_items):
        """builds a single table showcasing the trading house and cargo hold inventory inline listed by unique item rows, this is useful for comparing the market prices and the players inventory costs to determine what to buy or sell

        Args:
            market_items (list[MarketItems]): _description_
            player_items (list[PlayerItems]): _description_

        Returns:
            _type_: _description_
        """

        table = Table(title="Market and Inventory")
        table.add_column("#", justify="right")
        table.add_column("Trade Good", justify="left")
        table.add_column("Market Qty", justify="right")
        table.add_column("Market Price", justify="right")
        table.add_column("Cargo Qty", justify="right")
        table.add_column("Cargo Cost/Unit", justify="right")
        table.add_column("Total Cost", justify="right")
        table.add_column("Market Value", justify="right")

        cargo_hold_dict = {item.item_name: item for item in cargo_hold_items}

        for index, market_item in enumerate(trading_house_items):
            cargo_item = cargo_hold_dict.get(market_item.item_name)
            cargo_quantity = cargo_item.quantity if cargo_item else 0
            cargo_cost_per_unit = cargo_item.cost if cargo_item else 0
            total_cost = cargo_quantity * cargo_cost_per_unit
            total_value = cargo_quantity * market_item.price

            table.add_row(
                str(index + 1),
                market_item.item_name.title(),
                str(market_item.quantity),
                f"{market_item.price}",
                str(cargo_quantity),
                f"{cargo_cost_per_unit}",
                f"{total_cost}",
                f"{total_value}"
            )
        return table

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
            self.user_last_action = "Quit"
            self.menu_selection = 'q'
        else:
            print("Invalid input.")

    def title_screen(self):
        title = Panel.fit(f"{'PyMerchant':^30}\n" +
                          "A Hanseatic Trade League Simulation")
        print(title)
        input("Press enter to continue")
