from __future__ import annotations
from typing import Literal
from dataclasses import dataclass, field
from enumerations import TradeGoods, TradeGoodsCategory, MARKET_GOODS
from datetime import datetime


@dataclass(kw_only=True)
class Transaction:
    """
    Class that describes a Transaction object, used to track the history of a PlayerItem
    """
    price: int
    quantity: int
    type_of_transaction: Literal['buy', 'sell']
    date: datetime


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
    cost: float = 0
    last_seen_price: int = 0
    last_purchase_price: int = 0
    last_purchase_quantity: int = 0
    # last_seen_demand: DemandLevel = DemandLevel.NORMAL
    last_sale_price: int = 0
    last_sale_quantity: int = 0
    transaction_history: list[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)
        self.update_item_cost()

    def update_item_cost(self):
        # use transaction_history to build out an average cost, computed as the sum of all costs divided by the number of purchases, has a rolling average effect so that the user can sell items and then buy more at a different price and the average will reflect this
        total_cost = 0
        total_quantity = 0

        for transaction in self.transaction_history:
            if transaction.type_of_transaction == 'buy':
                total_cost += transaction.price * transaction.quantity
                total_quantity += transaction.quantity

        if total_quantity > 0:
            self.cost = total_cost / total_quantity
        else:
            self.cost = 0

    def check_sell(self):
        output = bool
        if self.quantity > 0:
            output = True
        else:
            output = False
        return output


@dataclass()
class MarketItem(Item):
    """
    Class that describes a MarketItem object, inherits from Item

    """
    price: int = 0
    # demand: DemandLevel = DemandLevel.NORMAL
    # supply: SupplyLevel = SupplyLevel.NORMAL
    # previous_price: int = 0
    # previous_quantity: int = 0
    # previous_day_demand: DemandLevel = DemandLevel.NORMAL
    # previous_day_supply: SupplyLevel = SupplyLevel.NORMAL

    def __post_init__(self):
        """

        """
        self.sigma = MARKET_GOODS[self.item_name]['sigma']
        self.mu = MARKET_GOODS[self.item_name]['mu']

    def check_buy(self, buy_qty, player_gold):
        output = bool
        if buy_qty <= self.quantity and player_gold >= buy_qty * self.price:
            output = True
        else:
            output = False
        return output
