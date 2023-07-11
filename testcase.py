from __future__ import annotations
from dataclasses import dataclass, field

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


@dataclass()
class Inventory:
    gold: int
    goods: dict = field(default_factory=dict)

    def __init__(self, gold, goods=None):
        self.gold = gold
        self.goods = goods or dict()
        self.build_inventory()

    def build_inventory(self):
        # build inventory from MARKET_GOODS
        # for each item in MARKET_GOODS, create an Item object
        # add the Item object to the inventory
        # note: each item needs to be accessible via attributes in Inventory object
        for item_name, item_info in MARKET_GOODS.items():
            item = Item(name=item_name, quantity=0,
                        category=item_info['category'], inputs=item_info['inputs'])
            self.goods[item_name] = item

    def get_item(self, item_name):
        return self.goods.get(item_name)


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

    print(market_inv.goods)
    print("\n\n\n")
    print(market_inv.goods['mead'])


if __name__ == '__main__':
    main()
