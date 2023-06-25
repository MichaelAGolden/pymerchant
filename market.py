

class Market:

    market_types = {
        "general_town": {
            "name": "General Town",
            "good_produced": ["wood", "stone", "iron", "grain", "wool", "leather"],
            "buildings": ["Town Hall", "Inn", "Blacksmith", "Stable", "Market"],
            "base_inventory": {"wood": 100, "stone": 100, "iron": 100, "grain": 100, "wool": 100, "leather": 100},
            "base_price": {"wood": 5, "stone": 20, "iron": 40, "grain": 3, "wool": 7, "leather": 10},
        },
        "farming_town": {
            "name": "Farming Town",
            "good_produced": ["grain", "wool", "leather"],
            "buildings": ["Town Hall", "Inn", "Blacksmith", "Stable", "Market"],
            "base_inventory": {"grain": 100, "wool": 100, "leather": 100},
            "base_price": {"grain": 1, "wool": 6, "leather": 20},
        },
        "mining_town": {
            "name": "Mining Town",
            "good_produced": ["stone", "iron"],
            "buildings": ["Town Hall", "Inn", "Blacksmith", "Stable", "Market"],
            "base_inventory": {"stone": 100, "iron": 100},
            "base_price": {"stone": 10, "iron": 15},
        }
    }

    ITEM_LIST = {
        "wood": {'name': "Wood", "weight_multiple": .5, "base_price": 5, "occurrence": "common", "base_quantity": 100},
        "stone": {'name': "Stone", "weight_multiple": 1.0, "base_price": 20, "occurrence": "common", "base_quantity": 100},
        "iron": {'name': "Iron", "weight_multiple": 0.8, "base_price": 40, "occurrence": "common", "base_quantity": 100},
        "grain": {'name': "Grain", "weight_multiple": 0.1, "base_price": 3, "occurrence": "common", "base_quantity": 100},
        "wool": {'name': "Wool", "weight_multiple": .6, "base_price": 7, "occurrence": "common", "base_quantity": 100},
        "leather": {'name': "Leather", "weight_multiple": .7, "base_price": 10, "occurrence": "common", "base_quantity": 100}
    }

    def __init__(self, name, connected_cities, market_type):
        self.name = name
        self.connected_cities = connected_cities
        self.market_type = self.market_types[market_type]
        self.market_inventory = self.market_type["base_inventory"]
        self.market_price = self.market_type["base_price"]
        self.market_buildings = self.market_type["buildings"]
        self.market_goods = self.market_type["good_produced"]

    def __repr__(self):
        return self.name

    def get_market_listings(self):
        table = list()
        for good, price in self.market_price.items():
            table.append([good, self.market_inventory[good], price])
        return table
