from dataclasses import dataclass
from datetime import datetime, timedelta
from tradeentity import City, Player
from enumerations import CITIES


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

    def update_city_inventories(self) -> None:
        """
        Function to update inventory supply level and pricing for all cities in the game, to be run ONLY once per game day
        """
        # for city in self.list_of_cities():
        #     Economy.update_supply(city)
        #     Economy.update_demand(city)
        #     Economy.update_pricing(city)
        pass
