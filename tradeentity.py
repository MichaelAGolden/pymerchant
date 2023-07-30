from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from enumerations import CITIES
from inventory import MarketInv, PlayerInv
# from modifiers import TravelModifier


@dataclass()
class Player:
    """
    Describes Player object
    Player does have access to the City object the player is located in
    Player also has access to their PlayerInv

    Care is needed to not inadvertently call a cities inventory self.location.inv instead of self.inv
    """
    location: City
    travel_mod_list: list
    travel_speed = nautical_miles_per_hour = 6
    inv: PlayerInv = field(default_factory=PlayerInv)

    @classmethod
    def get_time_to_travel(cls, player: Player, origin: City, destination: City):
        time: timedelta
        origin_name = origin.name
        destination_name = destination.name
        # modlist = []

        # lookup distance
        destination_distance = CITIES[origin_name].get(
            'distances', {}).get(destination_name)

        # # check player state for upgrades
        # if TravelModifier.get_travel_modifiers(player):
        #     for mod in TravelModifier.get_travel_modifiers(player):
        #         modlist.append(mod)
        #         print(mod)
        # if TravelModifier.get_travel_modifiers(origin):
        #     for mod in TravelModifier.get_travel_modifiers(origin):
        #         modlist.append(mod)
        #         print(mod)
        # if TravelModifier.get_travel_modifiers(destination):
        #     for mod in TravelModifier.get_travel_modifiers(destination):
        #         modlist.append(mod)
        #         print(mod)

        # total_percentage = 1
        # for mod in modlist:
        #     total_percentage += mod.speed
        # # sum modlist

        # randomize the travel time
        speed = 1 * cls.nautical_miles_per_hour
        time_to_travel = destination_distance / speed

        time = timedelta(hours=time_to_travel)

        return time


@dataclass()
class City:
    """
    Describes City Object
    """
    name: str
    travel_mod_list: list
    inv: MarketInv = field(default_factory=MarketInv)

    def sort_closest_cities(self, city_list=CITIES) -> dict[str, int]:
        """
        Sorting function for cities by distance.

        Note: Each distance in the CITIES dictionary was measured by hand from city to city in Google Earth in Nautical Miles by a novice approximation of a sea route.

        Likely these numbers are far off what real maritime sailing distance approximations would be, but I did not have the experience or time to write a program to approximate these distances for me.

        Nevertheless, these approximations are much more accurate than a as the crow flies measure between cities.

        sorting function uses lambda, pythons anoymous function generator
        lambda returns a value to be used as the key to sort the the list with the second position in the tuple index as the key

        Args:
            citylist (dict[str: dict[str, Any]]): Dictionary of cities with their coorresponding production attributes, used to build City objects. Defaults to CITIES.

        Returns:
            dict[str, int]: _description_
        """
        city_list_copy = city_list[self.name]['distances'].copy()

        sorted_city_list = dict(
            sorted(city_list_copy.items(), key=lambda tuple_from_items: tuple_from_items[1]))

        return sorted_city_list
