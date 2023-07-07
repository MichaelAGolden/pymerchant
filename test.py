
class Inventory:

    def __init__(self, name):
        self.name = name


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

flat_MARKET_GOODS = {good: properties
                     for category in MARKET_GOODS.values()
                     for good, properties in category.items()}
base_prices = {good: properties['base_price']
               for good, properties in flat_MARKET_GOODS.items()}

print(base_prices)
