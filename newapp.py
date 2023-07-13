from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from copy import copy, deepcopy


MARKET_GOODS = {
    'linen': {'inputs': ['hemp', 'flax'], 'base_price': 10, 'category': 'textiles'},
    'broadcloth': {'inputs': ['wool', 'dyes'], 'base_price': 100, 'category': 'textiles'},
    'clothing': {'inputs': ['linen', 'wool', 'pelts', 'dyes'], 'base_price': 120, 'category': 'textiles'},
    'wood': {'inputs': [None], 'base_price': 30, 'category': 'forestry'},
    'charcoal': {'inputs': ['wood'], 'base_price': 50, 'category': 'forestry'},
    'pitch': {'inputs': ['wood'], 'base_price': 80, 'category': 'forestry'},
    'grain': {'inputs': [None], 'base_price': 30, 'category': 'farming'},
    'honey': {'inputs': [None], 'base_price': 50, 'category': 'farming'},
    'hemp': {'inputs': [None], 'base_price': 80, 'category': 'farming'},
    'flax': {'inputs': [None], 'base_price': 50, 'category': 'farming'},
    'spices': {'inputs': [None], 'base_price': 200, 'category': 'farming'},
    'dyes': {'inputs': [None], 'base_price': 120, 'category': 'farming'},
    'wine': {'inputs': [None], 'base_price': 150, 'category': 'alcohol'},
    'mead': {'inputs': ['honey'], 'base_price': 80, 'category': 'alcohol'},
    'beer': {'inputs': ['grain'], 'base_price': 60, 'category': 'alcohol'},
    'fish': {'inputs': ['salt'], 'base_price': 60, 'category': 'fishing'},
    'salt': {'inputs': [None], 'base_price': 50, 'category': 'fishing'},
    'oil': {'inputs': ['fish'], 'base_price': 100, 'category': 'fishing'},
    'meat': {'inputs': ['salt'], 'base_price': 120, 'category': 'ranching'},
    'cheese': {'inputs': ['salt'], 'base_price': 200, 'category': 'ranching'},
    'pelts': {'inputs': [None], 'base_price': 150, 'category': 'ranching'},
    'wool': {'inputs': [None], 'base_price': 90, 'category': 'ranching'},
    'iron': {'inputs': [None], 'base_price': 100, 'category': 'mining'},
    'gems': {'inputs': [None], 'base_price': 400, 'category': 'mining'},
    'tools': {'inputs': ['wood', 'iron', ], 'base_price': 150, 'category': 'manufactured_items'},
    'weapons': {'inputs': ['wood', 'iron', 'tools'], 'base_price': 200, 'category': 'manufactured_items'},
    'armor': {'inputs': ['wood', 'iron', 'tools', 'clothing'], 'base_price': 300, 'category': 'manufactured_items'},
    'jewelry': {'inputs': ['iron', 'gems', 'tools'], 'base_price': 1000, 'category': 'manufactured_items'},
    'furniture': {'inputs': ['wood', 'linen', 'pelts', 'iron'], 'base_price': 200, 'category': 'manufactured_items'}
}

CITIES = {
    'antwerp': {
        'region': 'english_channel',
        'distances': {
            'bruges': 58,
            'bergen': 667,
            'bremen': 397,
            'cologne': 283,
            'danzig': 936,
            'hamburg': 373,
            'kampen': 202,
            'london': 182,
            'lubeck': 704,
            'malmo': 669,
            'novorod': 1614,
            'riga': 1198,
            'rostock': 777,
            'stockholm': 1142,
            'stralsund': 779,
            'tallinn': 1246,
            'visby': 1020},
        'productions': {
            'textiles': ['linen', 'clothing'],
            'farming': ['hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']
        }},
    'bruges': {
        'region': 'english_channel',
        'distances': {
            'antwerp': 58,
            'bergen': 559,
            'bremen': 320,
            'cologne': 208,
            'danzig': 901,
            'hamburg': 344,
            'kampen': 148,
            'london': 130,
            'lubeck': 749,
            'malmo': 642,
            'novorod': 1511,
            'riga': 1098,
            'rostock': 729,
            'stockholm': 1032,
            'stralsund': 718,
            'tallinn': 1155,
            'visby': 914},
        'productions': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'spices', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']
        }},
    'bergen': {
        'region': 'north_sea',
        'distances': {
            'antwerp': 667,
            'bruges': 559,
            'bremen': 480,
            'cologne': 658,
            'danzig': 726,
            'hamburg': 473,
            'kampen': 491,
            'london': 596,
            'lubeck': 568,
            'malmo': 466,
            'novorod': 1372,
            'riga': 953,
            'rostock': 556,
            'stockholm': 886,
            'stralsund': 541,
            'tallinn': 1009,
            'visby': 752},
        'productions': {
            'fishing': ['fish', 'oil'],
            'forestry': ['wood', 'charcoal', 'pitch']
        }},
    'bremen': {
        'region': 'north_sea',
        'distances': {
            'antwerp': 397,
            'bruges': 320,
            'bergen': 480,
            'cologne': 426,
            'danzig': 751,
            'hamburg': 116,
            'kampen': 216,
            'london': 393,
            'lubeck': 597,
            'malmo': 495,
            'novorod': 1357,
            'riga': 948,
            'rostock': 584,
            'stockholm': 864,
            'stralsund': 575,
            'tallinn': 995,
            'visby': 764},
        'productions': {
            'alcohol': ['mead', 'beer', 'wine'],
            'ranching': ['pelts', 'wool', 'cheese'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey']
        }},
    'cologne': {
        'region': 'english_channel',
        'distances': {
            'antwerp': 283,
            'bruges': 208,
            'bergen': 658,
            'bremen': 426,
            'danzig': 999,
            'hamburg': 446,
            'kampen': 261,
            'london': 297,
            'lubeck': 849,
            'malmo': 746,
            'novorod': 1605,
            'riga': 1201,
            'rostock': 839,
            'stockholm': 1003,
            'stralsund': 825,
            'tallinn': 1244,
            'visby': 1014},
        'productions': {
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey', 'spices'],
            'alcohol': ['wine', 'beer', 'mead']}},
    'danzig': {
        'region': 'south_baltic',
        'distances': {
            'antwerp': 935,
            'bruges': 901,
            'bergen': 726,
            'bremen': 751,
            'cologne': 999,
            'hamburg': 739,
            'kampen': 796,
            'london': 1089,
            'lubeck': 323,
            'malmo': 261,
            'novorod': 754,
            'riga': 328,
            'rostock': 277,
            'stockholm': 312,
            'stralsund': 245,
            'tallinn': 399,
            'visby': 210},
        'productions': {
            'farming': ['grain', 'hemp', 'flax', 'honey'],
            'mining': ['iron', 'gems'], }
    },
    'hamburg': {
        'region': 'north_sea',
        'distances': {
            'antwerp': 373,
            'bruges': 344,
            'bergen': 473,
            'bremen': 116,
            'cologne': 446,
            'danzig': 739,
            'kampen': 231,
            'london': 421,
            'lubeck': 612,
            'malmo': 503,
            'novorod': 1354,
            'riga': 958,
            'rostock': 593,
            'stockholm': 884,
            'stralsund': 579,
            'tallinn': 1004,
            'visby': 777},
        'productions': {
            'manufactured_items': ['jewelry', 'furniture'],
            'fishing': ['fish, oil, salt']
        }
    },
    'kampen': {
        'region': 'north_sea',
        'distances': {
            'antwerp': 202,
            'bruges': 148,
            'bergen': 491,
            'bremen': 216,
            'cologne': 261,
            'danzig': 796,
            'hamburg': 231,
            'london': 257,
            'lubeck': 653,
            'malmo': 550,
            'novorod': 1395,
            'riga': 999,
            'rostock': 642,
            'stockholm': 910,
            'stralsund': 625,
            'tallinn': 1041,
            'visby': 813},
        'productions': {
            'manufactured_items': ['jewelry', 'furniture'],
            'fishing': ['fish, oil, salt']}
    },
    'london': {
        'region': 'english_channel',
        'distances': {
            'antwerp': 182,
            'bruges': 130,
            'bergen': 596,
            'bremen': 393,
            'cologne': 297,
            'danzig': 1089,
            'hamburg': 421,
            'kampen': 257,
            'lubeck': 835,
            'malmo': 710,
            'novorod': 1609,
            'riga': 1180,
            'rostock': 826,
            'stockholm': 790,
            'stralsund': 802,
            'tallinn': 1235,
            'visby': 993},
        'productions': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey']},
    },
    'lubeck': {
        'region': 'south_baltic',
        'distances': {
            'antwerp': 704,
            'bruges': 749,
            'bergen': 568,
            'bremen': 597,
            'cologne': 849,
            'danzig': 323,
            'hamburg': 612,
            'kampen': 653,
            'london': 835,
            'malmo': 141,
            'novorod': 955,
            'riga': 547,
            'rostock': 61,
            'stockholm': 469,
            'stralsund': 107,
            'tallinn': 598,
            'visby': 365},
        'productions': {
            'fishing': ['salt', 'fish', 'oil'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture']}
    },
    'malmo': {
        'region': 'south_baltic',
        'distances': {
            'antwerp': 669,
            'bruges': 642,
            'bergen': 466,
            'bremen': 495,
            'cologne': 746,
            'danzig': 261,
            'hamburg': 503,
            'kampen': 550,
            'london': 710,
            'lubeck': 141,
            'novorod': 861,
            'riga': 453,
            'rostock': 98,
            'stockholm': 370,
            'stralsund': 83,
            'tallinn': 499,
            'visby': 269},
        'productions': {
            'forestry': ['wood', 'charcoal', 'pitch'],
            'fishing': ['fish', 'oil', 'salt'],
            'manufactured_items': ['tools' 'weapons', 'armor']}
    },
    'novorod': {
        'region': 'north_baltic',
        'distances': {
            'antwerp': 1614,
            'bruges': 1511,
            'bergen': 1372,
            'bremen': 1357,
            'cologne': 1605,
            'danzig': 754,
            'hamburg': 1354,
            'kampen': 1395,
            'london': 1609,
            'lubeck': 955,
            'malmo': 861,
            'riga': 551,
            'rostock': 900,
            'stockholm': 564,
            'stralsund': 868,
            'tallinn': 371,
            'visby': 600},
        'productions': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems']}
    },
    'riga': {
        'region': 'north_baltic',
        'distances': {
            'antwerp': 1198,
            'bruges': 1098,
            'bergen': 953,
            'bremen': 948,
            'cologne': 1201,
            'danzig': 328,
            'hamburg': 958,
            'kampen': 999,
            'london': 1180,
            'lubeck': 547,
            'malmo': 453,
            'novorod': 551,
            'rostock': 498,
            'stockholm': 240,
            'stralsund': 467,
            'tallinn': 187,
            'visby': 222},
        'productions': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'mining': ['iron', 'gems'],
            'forestry': ['wood', 'charcoal', 'pitch']},
    },
    'rostock': {
        'region': 'south_baltic',
        'distances': {
            'antwerp': 777,
            'bruges': 729,
            'bergen': 556,
            'bremen': 584,
            'cologne': 839,
            'danzig': 277,
            'hamburg': 593,
            'kampen': 642,
            'london': 826,
            'lubeck': 61,
            'malmo': 98,
            'novorod': 900,
            'riga': 498,
            'stockholm': 407,
            'stralsund': 58,
            'tallinn': 537,
            'visby': 307},
        'productions': {'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
                        'ranching': ['meat', 'cheese', 'pelts', 'wool'],
                        'fishing': ['fish', 'salt']}
    },
    'stockholm': {
        'region': 'north_baltic',
        'distances': {
            'antwerp': 1142,
            'bruges': 1032,
            'bergen': 886,
            'bremen': 864,
            'cologne': 1003,
            'danzig': 312,
            'hamburg': 884,
            'kampen': 910,
            'london': 790,
            'lubeck': 469,
            'malmo': 370,
            'novorod': 564,
            'riga': 240,
            'rostock': 407,
            'stralsund': 375,
            'tallinn': 206,
            'visby': 110},
        'productions': {
            'mining': ['iron', 'gems'],
            'forestry': ['wood', 'charcoal', 'pitch']},
    },
    'stralsund': {
        'region': 'south_baltic',
        'distances': {
            'antwerp': 779,
            'bruges': 718,
            'bergen': 541,
            'bremen': 575,
            'cologne': 825,
            'danzig': 245,
            'hamburg': 579,
            'kampen': 625,
            'london': 802,
            'lubeck': 107,
            'malmo': 83,
            'novorod': 868,
            'riga': 467,
            'rostock': 58,
            'stockholm': 375,
            'tallinn': 503,
            'visby': 272},
        'productions': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'spices', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']}
    },
    'tallinn': {
        'region': 'north_baltic',
        'distances': {
            'antwerp': 1246,
            'bruges': 1155,
            'bergen': 1009,
            'bremen': 995,
            'cologne': 1244,
            'danzig': 399,
            'hamburg': 1004,
            'kampen': 1041,
            'london': 1235,
            'lubeck': 598,
            'malmo': 499,
            'novorod': 371,
            'riga': 187,
            'rostock': 537,
            'stockholm': 206,
            'stralsund': 503,
            'visby': 239},
        'productions': {
            'fishing': ['fish', 'oil'],
            'forestry': ['wood', 'charcoal', 'pitch']}
    },
    'visby': {
        'region': 'north_baltic',
        'distances': {
            'antwerp': 1020,
            'bruges': 914,
            'bergen': 752,
            'bremen': 764,
            'cologne': 1014,
            'danzig': 210,
            'hamburg': 777,
            'kampen': 813,
            'london': 993,
            'lubeck': 365,
            'malmo': 269,
            'novorod': 600,
            'riga': 222,
            'rostock': 307,
            'stockholm': 110,
            'stralsund': 272,
            'tallinn': 239},
        'productions': {
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey', 'spices'],
            'alcohol': ['wine', 'beer', 'mead']}}
}


class TradeGoods(Enum):
    LINEN = 'linen'
    BROADCLOTH = 'broadcloth'
    CLOTHING = 'clothing'
    WOOD = 'wood'
    CHARCOAL = 'charcoal'
    PITCH = 'pitch'
    GRAIN = 'grain'
    HONEY = 'honey'
    HEMP = 'hemp'
    FLAX = 'flax'
    SPICES = 'spices'
    DYES = 'dyes'
    WINE = 'wine'
    MEAD = 'mead'
    BEER = 'beer'
    FISH = 'fish'
    SALT = 'salt'
    OIL = 'oil'
    MEAT = 'meat'
    CHEESE = 'cheese'
    PELTS = 'pelts'
    WOOL = 'wool'
    IRON = 'iron'
    GEMS = 'gems'
    TOOLS = 'tools'
    WEAPONS = 'weapons'
    ARMOR = 'armor'
    JEWELRY = 'jewelry'
    FURNITURE = 'furniture'


class TradeGoodsCategory(Enum):
    TEXTILES = 'textiles'
    FORESTRY = 'forestry'
    FARMING = 'farming'
    ALCOHOL = 'alcohol'
    FISHING = 'fishing'
    RANCHING = 'ranching'
    MINING = 'mining'
    MANUFACTURED_ITEMS = 'manufactured_items'


class DemandLevel(Enum):
    ABSENT = auto()
    LOW = auto()
    REDUCED = auto()
    NORMAL = auto()
    ELEVATED = auto()
    HIGH = auto()
    EXTREME = auto()


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
        return self.quantity

    def update_quantity(self, new_value) -> None:
        self.quantity = new_value

    def get_item_category(self) -> str:
        return self.category

    def get_item_inputs(self) -> list[str]:
        return self.inputs


@dataclass()
class PlayerItem(Item):
    last_seen_price: int = 0
    last_purchase_price: int = 0
    last_purchase_quantity: int = 0
    last_seen_demand: DemandLevel = None
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
    current_price: int = 0
    current_demand: DemandLevel = None
    previous_day_price: int = 0
    previous_day_quantity: int = 0
    previous_day_demand: DemandLevel = None


@dataclass()
class Inventory:
    # base inventory class used to define goods

    def get_item(self, item: str) -> Item:
        return getattr(self, item)

    def get_list_of_items(self):
        return [items for items in self.__dict__]

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


class ConsoleView:
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

    pass


class Economy:
    # Market pricing mechanics
    # sets demands, initial supply
    # updates economy as

    # for city in all_cities:
    #         for item in city.inventory:
    #         new_price = Economy.pricing(city, item)
    #         new_quantity = Economy.supply(city, item)
    #         item.update_quantity(new_quantity)
    #         item.update_price(new_price)

    def pricing(self, city, item):
        pass

    def supply(self, city, item):
        pass


class Gameloop:
    # all game logic ends up in here
    pass


def main():
    test = Inventory()
    print(test)
    lubeck = City('lubeck')
    maventa = Player('Maventa', lubeck)

    print(maventa.location.sort_closest_cities())


if __name__ == "__main__":
    main()
