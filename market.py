import random


class Market:

    # 1st level of market dict is the market type
    # 2nd level of market dict is the market good
    # 3rd level of market dict is the market good's inputs and prices
    MARKET_GOODS = {
        'textiles': {
            'linen': {'inputs': ['hemp', 'flax'], 'base_price': 10},
            'broadcloth': {'inputs': ['wool', 'dyes'], 'base_price': 100},
            'clothing': {'inputs': ['linen', 'wool', 'pelts', 'dyes'], 'base_price': 120}
        },
        'forestry': {
            'wood': {'inputs': [None], 'base_price': 30},
            'charcoal': {'inputs': ['wood'], 'base_price': 50},
            'pitch': {'inputs': ['wood'], 'base_price': 80}
        },
        'farming': {
            'grain': {'inputs': [None], 'base_price': 30},
            'honey': {'inputs': [None], 'base_price': 50},
            'hemp': {'inputs': [None], 'base_price': 80},
            'flax': {'inputs': [None], 'base_price': 50},
            'spices': {'inputs': [None], 'base_price': 200},
            'dyes': {'inputs': [None], 'base_price': 120}
        },
        'alcohol': {
            'wine': {'inputs': [None], 'base_price': 150},
            'mead': {'inputs': ['honey'], 'base_price': 80},
            'beer': {'inputs': ['grain'], 'base_price': 60}
        },
        'fishing': {
            'fish': {'inputs': ['salt'], 'base_price': 60},
            'salt': {'inputs': [None], 'base_price': 50},
            'oil': {'inputs': ['fish'], 'base_price': 100}
        },
        'ranching': {
            'meat': {'inputs': ['salt'], 'base_price': 120},
            'cheese': {'inputs': ['salt'], 'base_price': 200},
            'pelts': {'inputs': [None], 'base_price': 150},
            'wool': {'inputs': [None], 'base_price': 90}
        },
        'mining': {
            'iron': {'inputs': [None], 'base_price': 100},
            'gems': {'inputs': [None], 'base_price': 400}
        },
        'manufactured_items': {
            'tools': {'inputs': ['wood', 'iron', 'stone'], 'base_price': 150},
            'weapons': {'inputs': ['wood', 'iron', 'stone', 'tools'], 'base_price': 200},
            'armor': {'inputs': ['wood', 'iron', 'stone', 'tools', 'clothing'], 'base_price': 300},
            'jewelry': {'inputs': ['iron', 'gems', 'tools', 'stone'], 'base_price': 1000},
            'furniture': {'inputs': ['wood', 'linen', 'pelts', 'iron'], 'base_price': 200}
        }
    }

    # List of CITIES and their distances from each other, in nautical miles by sea, charted by hand in google earth
    CITIES_DISTANCES = {
        'antwerp': {
            'bruges': 58,
            'bergen': 667,
            'bremen': 397,
            'cologne': 283,
            'danzig': 936,
            'hamburg': 373,
            'kampen': 202.,
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
        'bruges': {
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
        'bergen': {
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
        'bremen': {
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
        'cologne': {
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
        'danzig': {
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
        'hamburg': {
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
        'kampen': {
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
        'london': {
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
        'lubeck': {
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
        'malmo': {
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
        'novorod': {
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
        'riga': {
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
        'rostock': {
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
        'stockholm': {
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
        'stralsund': {
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
        'tallinn': {
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
        'visby': {
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
            'tallinn': 239}}

    # List of CITIES and their region name
    # Built by using k-means cluster on the cities cities distances from one another from CITIES_DISTANCES
    CITIES_REGIONS = {
        'north_baltic': ['novorod', 'riga', 'tallinn', 'stockholm', 'visby'],
        'south_baltic': ['malmo', 'lubeck', 'rostock', 'stralsund', 'danzig'],
        'north_sea': ['bergen', 'bremen', 'hamburg', 'kampen'],
        'english_channel': ['antwerp', 'bruges', 'cologne', 'london'],
    }

    CITIES_PRODUCTIONS = {
        'antwerp': {
            'textiles': ['linen', 'clothing'],
            'farming': ['hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']
        },
        'bruges': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'spices', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']
        },
        'bergen': {
            'fishing': ['fish', 'oil'],
            'forestry': ['wood', 'charcoal', 'pitch'],
        },
        'bremen': {
            'alcohol': ['mead', 'beer', 'wine'],
            'ranching': ['pelts', 'wool', 'cheese'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
        },
        'cologne': {
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey', 'spices'],
            'alcohol': ['wine', 'beer', 'mead']
        },
        'danzig': {
            'farming': ['grain', 'hemp', 'flax', 'honey'],
            'mining': ['iron', 'gems'],
        },
        'hamburg': {
            'fishing': ['fish', 'oil', 'salt'],
            'manufactured_items': ['tools', 'weapons', 'armor']
        },
        'kampen': {
            'manufactured_items': ['jewelry', 'furniture'],
            'fishing': ['fish, oil, salt'],
        },
        'london': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
        },
        'lubeck': {
            'fishing': ['salt', 'fish', 'oil'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
        },
        'malmo': {
            'forestry': ['wood', 'charcoal', 'pitch'],
            'fishing': ['fish', 'oil', 'salt'],
            'manufactured_items': ['tools' 'weapons', 'armor'],
        },
        'novorod': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems'],
        },
        'riga': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'mining': ['iron', 'gems'],
            'forestry': ['wood', 'charcoal', 'pitch'],
        },
        'rostock': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'fishing': ['fish', 'salt'],
        },
        'stockholm': {
            'mining': ['iron', 'gems'],
            'forestry': ['wood', 'charcoal', 'pitch'],
        }
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
            table.append([good, price])
        return table

    def get_connected_cities(self):
        return self.connected_cities
