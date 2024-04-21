from __future__ import annotations
from dataclasses import dataclass
from random import normalvariate

from item import Item, PlayerItem, MarketItem
from enumerations import MARKET_GOODS


@dataclass()
class Inventory:
    """
    Class that describes an Inventory object, super class to PlayerInventory and MarketInventory
    """

    def __repr__(self) -> str:
        return f"{self.item}"

    def get_list_of_items(self) -> list[Item]:
        """
        Returns list of items in inventory

        Returns:
            list[Item]: list of Item objects
        """
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item)]

    def has_input(self, trade_good: str) -> list[Item]:
        """
        Returns list of items that have inputs of a given trade_good

        Args:
            trade_good (str): TradeGood

        Returns:
            list[Item]: List of Item objects
        """
        return [item for item in self.get_list_of_items(
        ) if trade_good in item.inputs]

    def has_category(self, trade_good_category: str) -> list[Item]:
        """
        Returns list of items that have a specific trade_good_category

        Args:
            trade_good_category (str): TradeGoodsCategory

        Returns:
            list[Item]: List of Item objects
        """
        return [item for item in self.get_list_of_items() if item.category is trade_good_category]


@dataclass(kw_only=True)
class PlayerInv(Inventory):
    """
    Class that describes a PlayerInventory object, inherits from Inventory

    """

    def __init__(self) -> None:
        """
        Initializes PlayerInventory
        """
        self.gold = 1000
        for item, info in MARKET_GOODS.items():
            trade_good = PlayerItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_player_item(self, item: str) -> PlayerItem:
        """
        Returns player_item via an accessor method.

        While not traditionally "pythonic" this prevents runtime errors if an item attribute is not a keyword property of the PlayerInventory

        Args:
            item (str): item name to lookup

        Returns:
            PlayerItem: The PlayerItem object
        """
        return getattr(self, item)

    def get_list_of_items(self) -> list[PlayerItem]:
        """
        Returns list of items of PlayerItem type in PlayerInventory

        Returns:
            list[PlayerItem]: PlayerItem Objects
        """
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), PlayerItem)]


@dataclass(kw_only=True)
class MarketInv(Inventory):
    """
    Class that describes an MarketInventory object, inherits from Inventory class
    """

    def __init__(self) -> None:
        """
        Initializes MarketInventory
        """
        for item, info in MARKET_GOODS.items():
            trade_good = MarketItem(item_name=item, quantity=100, price=100,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_list_of_items(self) -> list[MarketItem]:
        """
        Returns list of MarketItems in MarketInventory

        Returns:
            list[MarketItem]: MarketItem object
        """
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), MarketItem)]

    def get_market_item(self, item: str) -> MarketItem:
        """
        Returns player_item via an accessor method.

        While not traditionally "pythonic" this prevents runtime errors if an item attribute is not a keyword property of the PlayerInventory

        Args:
            item (str): item name to lookup

        Returns:
            PlayerItem: The PlayerItem object
        """
        return getattr(self, item)

    def get_market_data(self) -> dict[str, dict[str, int]]:
        """
        Returns a list of list of [item_name, item.price, item.quantity] for all items in market

        Returns:
            list[list[str,int,int]]: [[self.item_name, self.item.price, self.item.quantity]...[]]
        """
        market_inv = {}
        for item in self.get_list_of_items():
            name = item.item_name
            quantity = item.quantity
            price = item.price
            market_inv[name] = {'quantity': quantity, 'price': price}
        return market_inv

    def update_item_pricing(self):
        """_summary_
        """
        # placeholder value
        for item in self.get_list_of_items():
            item.price = round(normalvariate(item.mu, item.sigma))

    def update_item_quantity(self):
        # self.quantity = 100
        for item in self.get_list_of_items():
            item.quantity = 100
