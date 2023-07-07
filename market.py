
import random


class Market:


    # 1st level of market dict is the market type
    # 2nd level of market dict is the market good
    # 3rd level of market dict is the market good's inputs and prices
    MARKET_GOODS = {
        'textiles': {
            'linen': {'inputs': ['hemp', 'flax'], 'base_price': 10},
            'clothing': {'inputs': ['linen', 'wool', 'pelts', 'dyes'], 'base_price': 120}},
        'forestry': {
            'wood': {'inputs': [None], 'base_price': 30},
            'charcoal': {'inputs': ['wood'], 'base_price': 50},
            'pitch': {'inputs': ['wood'], 'base_price': 80}},
        'farming': {
            'grain': {'inputs': [None], 'base_price': 30},
            'honey': {'inputs': [None], 'base_price': 50},
            'hemp': {'inputs': [None], 'base_price': 80},
            'flax': {'inputs': [None], 'base_price': 50},
            'spices': {'inputs': [None], 'base_price': 200},
            'dyes': {'inputs': [None], 'base_price': 120}},
        'alcohol': {
            'wine': {'inputs': [None], 'base_price': 150},
            'mead': {'inputs': ['honey'], 'base_price': 80},
            'beer': {'inputs': ['grain'], 'base_price': 60}},
        'fishing': {
            'fish': {'inputs': ['salt'], 'base_price': 60},
            'salt': {'inputs': [None], 'base_price': 50},
            'oil': {'inputs': ['fish'], 'base_price': 50}},
        'ranching': {
            'meat': {'inputs': ['salt'], 'base_price': 120},
            'cheese': {'inputs': ['salt'], 'base_price': 200},
            'fish': {'inputs': ['salt'], 'base_price': 120},
            'pelts': {'inputs': [None], 'base_price': 150},
            'wool': {'inputs': [None], 'base_price': 90}},
        'mining': {
            'stone': {'inputs': [None], 'base_price': 50},
            'iron': {'inputs': [None], 'base_price': 100},
            'gems': {'inputs': [None], 'base_price': 400}},
        'manufactured_items': {
            'tools': {'inputs': ['wood', 'iron', 'stone'], 'base_price': 150},
            'weapons': {'inputs': ['wood', 'iron', 'stone', 'tools'], 'base_price': 200},
            'armor': {'inputs': ['wood', 'iron', 'stone', 'tools', 'clothing'], 'base_price': 300},
            'jewelry': {'inputs': ['iron', 'gems', 'tools', 'stone'], 'base_price': 1000},
            'furniture': {'inputs': ['wood', 'linen', 'pelts', 'iron'], 'base_price': 200}}
    }

    MARKET_CONNECTIONS = {
        'lubek': ['hamburg', 'bremen', 'berlin', 'rostock'],
        'hamburg': ['lubek', 'bremen', 'rostock'],
        'bremen': ['hamburg', 'berlin'],
        'berlin': ['lubek', 'bremen'],
        'rostock': ['lubek', 'berlin']

    }

    FLAT_MARKET_GOODS = {good: properties
                         for category in MARKET_GOODS.values()
                         for good, properties in category.items()}
    BASE_PRICES = {good: properties['base_price']
                   for good, properties in FLAT_MARKET_GOODS.items()}

    def __init__(self, name, market_tier, connected_cities=None,):
        self.name = name
        self.connected_cities = connected_cities
        self.market_tier = market_tier
        self.market_inventory = {}
        self.build_market()


    def __repr__(self):
        return self.name


    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.values):
            raise StopIteration
        value = self.values[self.index]
        self.index += 1
        return value

    def build_market(self, item_list=BASE_PRICES):

        def initial_quantity():
            rand_adjustment = random.normalvariate(0, .01)
            qty = 100 * self.market_tier + round(rand_adjustment)
            return qty

        def initial_price(item):
            base_price = item_list[item]
            standard_deviation = base_price * 0.1
            price = round(
                random.normalvariate(base_price, standard_deviation))
            return price

        for item in item_list:
            qty = initial_quantity()
            price = initial_price(item)
            self.market_inventory.update(
                {item: {'quantity': qty, 'price': price}})

    def get_market_listings(self):
        table = []
        for good, price in self.market_inventory.items():
            table.append([good, self.market_inventory[good], price])
        return table

    def get_connected_cities(self):
        return self.connected_cities

    def get_market_listings(self):
        table = list()
        for good, price in self.market_price.items():
            table.append([good, self.market_inventory[good], price])
        return table

