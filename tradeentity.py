from __future__ import annotations
from datetime import timedelta
from inventory import PlayerInv, MarketInv
from enumerations import CITIES
from item import MarketItem
from modifiers import TravelModifier
from dataclasses import dataclass, field
from scipy.optimize import fsolve
from scipy.stats import norm


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
        modlist = []

        # lookup distance
        destination_distance = CITIES[origin_name].get(
            'distances', {}).get(destination_name)

        # check player state for upgrades
        if TravelModifier.get_travel_modifiers(player):
            for mod in TravelModifier.get_travel_modifiers(player):
                modlist.append(mod)
                print(mod)
        if TravelModifier.get_travel_modifiers(origin):
            for mod in TravelModifier.get_travel_modifiers(origin):
                modlist.append(mod)
                print(mod)
        if TravelModifier.get_travel_modifiers(destination):
            for mod in TravelModifier.get_travel_modifiers(destination):
                modlist.append(mod)
                print(mod)

        total_percentage = 1
        for mod in modlist:
            total_percentage += mod.speed
        # sum modlist

        # randomize the travel time
        speed = total_percentage * cls.nautical_miles_per_hour
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

        Likely these numbers are far off what real maritime sailing distance approximations would be, but I did not have the experience or time to write a program to approximate these distances for me, and from my research, it seems that if you could write such a program, it could be a very lucrative endeavor as the paid programs for this are very expensive.

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

    def update_market(self, city):
        """
        Updates all prices for items in a given city

        Args:
            city (City): City we are updating
        """
        for item in city.inv.get_list_of_items():
            self.update_pricing(item)

    def update_pricing(self, item: MarketItem):
        """
        needs rework
        Args:
            item (MarketItem): _description_

        Returns:
            _type_: _description_
        """

        # class method to update individual item pricing at a market
        demand_mu = item.demand_mu
        demand_sigma = item.demand_sigma
        supply_mu = item.supply_mu
        supply_sigma = item.supply_sigma

        item.previous_price = item.price
        item.previous_quantity = item.quantity

        def demand(p, mu, sigma):
            return norm.sf(p, mu, sigma)

        def supply(p, mu, sigma):
            return norm.cdf(p, mu, sigma)

        def find_equilibrium(demand_mu, demand_sigma, supply_mu, supply_sigma):
            price_eq = fsolve(lambda p: supply(
                p, supply_mu, supply_sigma) - demand(p, demand_mu, demand_sigma), 0.5)
            quantity_eq = supply(price_eq, supply_mu, supply_sigma)

            # returns a tuple representing the given coordinates price(gold) and quantity(% of total city demand/production) that solves for the two functions of supply and demand
            coordinates = (price_eq[0], quantity_eq[0])
            return coordinates

        output = find_equilibrium(
            demand_mu, demand_sigma, supply_mu, supply_sigma)

        new_price = round(output[0])
        new_qty = round(output[1] * item.previous_quantity)

        item.quantity = new_qty
        item.price = new_price

    def update_supply(self, city, item):
        # previous_supply = city.market.item.get_supply()
        # price = city.market.item.price
        # demand = city.market.item.get_demand()
        pass

    def update_demand(self, city, item):
        # previous_demand = city.market.item.get_demand()
        # price = city.market.item.price()
        # supply = city.market.item.get_supply()
        pass
