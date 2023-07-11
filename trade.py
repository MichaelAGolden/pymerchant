from __future__ import annotations
from dataclasses import dataclass, field


def set_inventory(seller, buyer, item_name, item_qty):
    """
    set_inventory updates buyer and seller inventories at same in transaction

    Args:
        seller (Entity): Entity that is the seller in the context of the transaction
        buyer (Entity): Entity that is the buyer in the context of the transaction
        item_name (str): Name of item that is being traded
        item_qty (int): Quantity of item that is being traded
    """
    # updates seller item quantity
    prior_seller_item_qty = getattr(seller, item_name)
    updated_seller_item_qty = prior_seller_item_qty - item_qty
    setattr(seller, item_name, updated_seller_item_qty)

    # updates buyer item quantity
    prior_buyer_item_qty = getattr(buyer, item_name)
    updated_buyer_item_qty = prior_buyer_item_qty + item_qty
    setattr(buyer, item_name, updated_buyer_item_qty)


def set_gold(seller, buyer, total_trade):
    """
    set_gold updates buyer and seller gold attributes at same time in transaction

    Args:
        seller (Entity): Entity that is the seller in the context of the transaction
        buyer (Entity): Entity that is the buyer in the context of the transaction
        total_trade (int): Total trade value, represented as an integer value
    """
    # updates seller gold
    prior_seller_gold = getattr(seller, 'gold')
    updated_seller_gold = prior_seller_gold + total_trade
    setattr(seller, 'gold', updated_seller_gold)

    # updates buyer gold
    prior_buyer_gold = getattr(buyer, 'gold')
    updated_buyer_gold = prior_buyer_gold - total_trade
    setattr(buyer, 'gold', updated_buyer_gold)


def log_transaction(buyer, seller, item_name, item_price, item_qty):
    pass


def trade(user, city_market, trade_type, item_name, item_price, item_qty):
    total_trade = item_price * item_qty
    if trade_type == 'buy':
        buyer = user
        seller = city_market
    elif trade_type == 'sell':
        buyer = city_market
        seller = user
    set_gold(buyer, seller, total_trade)
    set_inventory(buyer, seller, item_name, item_qty)
    output = log_transaction(buyer, seller, item_name, item_qty, item_price)
    return output


# @dataclass()
# class Transaction:
#     """
#      _summary_
#      Transaction class provides class method provides a way to dynamically store transactions between player and markets as its own datatype, encapsulating all information necessary to understand the transaction and is the base input for all logging
#     """
#     buyer: object
#     seller: object
#     item_name: str
#     item_price: int
#     item_qty: int


@dataclass()
class Inventory:
    gold: int

    def __init__(self, gold):
        self.gold = gold
        self.build_inventory()

    def build_inventory(self):
        # build inventory from MARKET_GOODS
        # for each item in MARKET_GOODS, create an Item object
        # add the Item object to the inventory
        # note: each item needs to be accessible via attributes in Inventory object
        for item_name, item_info in MARKET_GOODS.items():
            item = Item(name=item_name, quantity=0,
                        category=item_info['category'], inputs=item_info['inputs'])
            setattr(self, item_name, item)

    # def get_item(self, item_name):
    #     return self.goods.get(item_name)


@dataclass()
class Item:
    name: str
    quantity: int
    category: str
    inputs: list = field(default_factory=list)

    def update_quantity(self, quantity):
        self.quantity = quantity

    def get_category(self):
        return self.category

    def get_inputs(self):
        return self.inputs


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


def main():
    # # test initialize some variables
    # linen = Item(name='linen', quantity=0,
    #              category='textiles', inputs=[None])
    # wool = Item(name='wool', quantity=0, category='textiles',
    #             inputs=[None])
    # print(linen)
    # print(wool)
    # #this works

    market_inv = Inventory(gold=1000)

    print(market_inv)
    print("\n\n\n")
    print(market_inv.__dir__())


if __name__ == '__main__':
    main()
