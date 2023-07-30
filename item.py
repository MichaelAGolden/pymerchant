from __future__ import annotations
from dataclasses import dataclass
from doctest import OutputChecker
from sys import exception
from enumerations import TradeGoods, TradeGoodsCategory, MARKET_GOODS, SupplyLevel, DemandLevel


@dataclass(kw_only=True)
class Item:
    """
    Class that describes an Item or "TradeGood", super class to PlayerItem and MarketItem
    """
    item_name: TradeGoods
    quantity: int
    category: TradeGoodsCategory
    inputs: list[TradeGoods]


@dataclass()
class PlayerItem(Item):
    """
    Class that describes a PlayerItem object, inherits from Item

    """
    cost = 0
    last_seen_price: int = 0
    last_purchase_price: int = 0
    last_purchase_quantity: int = 0
    last_seen_demand: DemandLevel = DemandLevel.NORMAL
    last_sale_price: int = 0
    last_sale_quantity: int = 0

    def check_sell(self, market_quantity):
        output = bool

        if self.quantity < market_quantity:
            output = False
        else:
            output = True
        return output


@dataclass()
class MarketItem(Item):
    """
    Class that describes a MarketItem object, inherits from Item

    """

    price: int = 0
    demand: DemandLevel = DemandLevel.NORMAL
    supply: SupplyLevel = SupplyLevel.NORMAL
    previous_price: int = 0
    previous_quantity: int = 0
    previous_day_demand: DemandLevel = DemandLevel.NORMAL
    previous_day_supply: SupplyLevel = SupplyLevel.NORMAL

    def __post_init__(self):
        """

        """
        self.demand_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.demand_mu = MARKET_GOODS[self.item_name]['base_price'] / 2
        self.supply_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.supply_mu = MARKET_GOODS[self.item_name]['base_price'] / 2

    def trade(self):
        pass

    def check_buy(self, buy_qty, player_gold):
        output = bool
        if buy_qty <= self.quantity and player_gold >= buy_qty * self.price:
            output = True
            print('passed check_buy')
        else:
            output = False
        return output
