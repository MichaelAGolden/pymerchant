from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from scipy.stats import norm
from scipy.optimize import fsolve


@dataclass()
class MarketEvent:
    event_type: Enum
    affected_region: Enum
    affected_city: Enum
    affected_category: Enum
    affected_trade_good: Enum
    time_to_expire: datetime
    time_sent: datetime

    @classmethod
    def check_rumor(cls, city, item):
        # return list of events in a city
        pass

    @classmethod
    def check_MarketEvent(cls):
        # delete market event if days remaining is 0
        # call delete market event function
        pass

    @classmethod
    def delete_MarketEvent(cls, mktevent):
        pass

    @classmethod
    def get_market_rumor(cls, game):
        # excluding current player city, return a marketevent from a city or region
        pass

    @classmethod
    def create_MarketEvent(cls, city, rumor):
        # check all marketevents at given city,
        # create new marketevent with UUID in the cities that it applies to
        # if one market event of the same exact kind already exists, just extend its duration by that number of days
        pass


@dataclass(kw_only=True)
class Item:
    # base item class used for handling construction of all trading goods
    # Used critically in the construction of the Inventory base classes
    item_name: str
    quantity: int
    category: str
    inputs: list[str]

    def get_item_name(self) -> str:
        return self.item_name

    def get_item_quantity(self) -> int:
        return getattr(self, 'quantity')

    def set_item_quantity(self, new_value) -> None:
        setattr(self, 'quantity', new_value)

    def get_item_category(self) -> str:
        return self.category

    def get_item_inputs(self) -> list[str]:
        return self.inputs


@dataclass()
class PlayerItem(Item):
    last_seen_price: int = 0
    last_purchase_price: int = 0
    last_purchase_quantity: int = 0
    last_seen_demand: DemandLevel = DemandLevel.NORMAL
    last_sale_price: int = 0
    last_sale_quantity: int = 0

    def set_last_seen_demand(self, demand: DemandLevel):
        self.last_seen_demand = demand

    def set_last_seen_price(self, price):
        self.last_seen_price = price

    def set_last_purchase_price(self, price):
        self.last_purchase_price = price

    def set_last_purchase_quantity(self, quantity):
        self.last_purchase_quantity = quantity

    def set_last_sale_price(self, price):
        self.last_sale_price = price

    def set_last_sale_quantity(self, quantity):
        self.last_purchase_price = quantity


@dataclass()
class MarketItem(Item):

    price: int = 0
    demand: DemandLevel = DemandLevel.NORMAL
    supply: SupplyLevel = SupplyLevel.NORMAL
    previous_price: int = 0
    previous_quantity: int = 0
    previous_day_demand: DemandLevel = DemandLevel.NORMAL
    previous_day_supply: SupplyLevel = SupplyLevel.NORMAL

    def __post_init__(self):
        self.demand_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.demand_mu = MARKET_GOODS[self.item_name]['base_price'] / 2
        self.supply_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.supply_mu = MARKET_GOODS[self.item_name]['base_price'] / 2

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price

    def set_previous_price(self, val):
        self.previous_price = val

    def set_previous_quantity(self, val):
        self.previous_quantity = val

    def set_demand_mu(self, val):
        setattr(self, 'demand_mu', val)

    def get_demand_mu(self):
        return getattr(self, 'demand_mu')

    def set_supply_mu(self, val):
        setattr(self, 'supply_mu', val)

    def get_supply_mu(self):
        return getattr(self, 'supply_mu')

    def set_demand_sigma(self, val):
        setattr(self, 'demand_sigma', val)

    def get_demand_sigma(self):
        return getattr(self, 'demand_sigma')

    def set_supply_sigma(self, val):
        setattr(self, 'supply_sigma', val)

    def get_supply_sigma(self):
        return getattr(self, 'supply_sigma')


@dataclass()
class Inventory:
    # base inventory class used to define goods

    def get_item(self, item: str) -> Item:
        return getattr(self, item)

    def get_list_of_items(self):
        return [items for items in dir(self) if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem) or isinstance(getattr(self, items), MarketItem)]

    def has_input(self, trade_good: str) -> list[str]:
        """
        has_input returns list of Item() names in Inventory that have trade_good as an input

        Args:
            trade_good (str): trade_good or Item() name

        Returns:
            list[str]:
        """
        return [item for item in self.get_list_of_items(
        ) if trade_good in self.get_item(item).inputs]

    def has_category(self, trade_good_category: str) -> list[str]:
        """
        Returns all items in a given category of goods in list

        Dependent on trade_good_category matching one of categories in MARKET_GOODS

        Args:
            trade_good_category (str):

        Returns:
            list[str]
        """
        return [item for item in self.get_list_of_items() if self.get_item(item).category is trade_good_category]


@dataclass(kw_only=True)
class PlayerInventory(Inventory):
    # inventory-like object for a player, inherits from Inventory

    def __init__(self) -> None:
        self.gold = 1000
        for item, info in MARKET_GOODS.items():
            trade_good = PlayerItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_player_item(self, item: str) -> PlayerItem:
        return getattr(self, item)

    def get_gold(self) -> int:
        return self.gold

    def set_gold(self, new_gold) -> None:
        self.gold = new_gold

    def get_capacity(self) -> int:
        return self.capacity

    def set_capacity(self, new_capacity) -> None:
        self.capacity = new_capacity


@dataclass(kw_only=True)
class Market(Inventory):
    # inventory-like object for use within a City object in game structure

    def __init__(self) -> None:
        for item, info in MARKET_GOODS.items():
            trade_good = MarketItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_market_item(self, item: str) -> MarketItem:
        return getattr(self, item)

    def get_market_data(self):
        market_info = list()
        for name in self.get_list_of_items():
            item: MarketItem = self.get_market_item(name)
            item_name = item.get_item_name()
            price = item.get_price()
            quantity = item.get_item_quantity()
            market_info.append([item_name, price, quantity])
        return market_info


class View:
    # handles all GUI aspects of game
    pass


class Travel:
    # Module handles travel between Cities

    def distance_to_days(self, city, distance, citylist=CITIES):
        pass


@dataclass()
class Player:
    # constructor player object
    name: str
    location: City
    inv: PlayerInventory = field(default_factory=PlayerInventory)


@dataclass()
class City:
    # city object contains
    # Market object
    # Market inherits Inventory contains Items
    name: str
    market: Market = field(default_factory=Market)

    def get_location_name(self):
        return self.name

    def sort_closest_cities(self, citylist=CITIES):
        citylist_copy = citylist[self.name]['distances'].copy()
        citylist_copy = dict(sorted(citylist_copy.items(), key=lambda x: x[1]))
        return citylist_copy


class Economy:
    # Market pricing mechanics
    # sets demands, initial supply
    # updates economy as

    @classmethod
    def update_market(cls, city):
        for item in city.market.get_list_of_items():
            itemlookup = city.market.get_item(item)
            cls.update_pricing(itemlookup)

    @classmethod
    def update_pricing(cls, item):
        # class method to update individual item pricing at a market
        demand_mu = item.get_demand_mu()
        demand_sigma = item.get_demand_sigma()
        supply_mu = item.get_supply_mu()
        supply_sigma = item.get_supply_sigma()
        old_price = item.get_price()
        old_qty = 100
        item.set_previous_price(old_price)
        item.set_previous_quantity(old_qty)

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
        new_qty = round(output[1] * old_qty)

        item.set_item_quantity(new_qty)
        item.set_price(new_price)

    @classmethod
    def update_supply(cls, city, item):
        # previous_supply = city.market.item.get_supply()
        # price = city.market.item.get_price()
        # demand = city.market.item.get_demand()
        pass

    @classmethod
    def update_demand(cls, city, item):
        # previous_demand = city.market.item.get_demand()
        # price = city.market.item.get_price()
        # supply = city.market.item.get_supply()
        pass


@dataclass()
class Game:
    starting_date = datetime(year=1393, month=7, day=29)
    # all game logic ends up in here

    def __init__(self, player_name='user', starting_city='lubeck', starting_date=starting_date) -> None:
        # setup all game objects at setattr
        self.player_name = player_name
        self.starting_city = starting_city
        self.current_date = starting_date
        self.build_cities()
        self.update_city_inventories()
        self.create_player()

    def advance_days(self, days_to_advance):
        setattr(self, 'current_date', days_to_advance)

    def build_cities(self) -> None:
        for city in CITIES.keys():
            new_city = City(city, market=Market())
            setattr(self, city, new_city)

    def create_player(self) -> None:
        city = self.get_city(self.starting_city)
        new_player = Player(self.player_name, city)
        setattr(self, self.player_name, new_player)
        pass

    def list_of_players(self):
        return getattr(self, 'player')

    def list_of_cities(self):
        return [city for city in dir(self) if isinstance(getattr(self, city), City)]

    def get_city(self, city: str):
        return getattr(self, city)

    def update_city_inventories(self) -> None:
        # for city in self.list_of_cities():
        #     Economy.update_supply(city)
        #     Economy.update_demand(city)
        #     Economy.update_pricing(city)
        pass

    def build_rumors(self):
        pass


def main():
    app = Game()
    for city in app.list_of_cities():
        lookupcity = app.get_city(city)
        Economy.update_market(lookupcity)

    for city in app.list_of_cities():
        lookupcity = app.get_city(city)
        print(lookupcity.market.get_market_data())


if __name__ == "__main__":
    main()
