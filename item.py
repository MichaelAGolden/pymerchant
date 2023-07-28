from __future__ import annotations
from dataclasses import dataclass
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
        Post init allows for us to set our demand and supply attributes following initial MarketItem init using @dataclass()

        Values are placeholders for now
        """
        self.demand_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.demand_mu = MARKET_GOODS[self.item_name]['base_price'] / 2
        self.supply_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.supply_mu = MARKET_GOODS[self.item_name]['base_price'] / 2
