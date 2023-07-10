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
            'bruges': 58.4,
            'bergen': 667.0,
            'bremen': 397.0,
            'cologne': 283.0,
            'danzig': 935.6,
            'hamburg': 372.6,
            'kampen': 201.6,
            'london': 182.2,
            'lubeck': 704.0,
            'malmo': 669.0,
            'novorod': 1614.0,
            'riga': 1198.0,
            'rostock': 777.0,
            'stockholm': 1142.0,
            'stralsund': 779.0,
            'tallinn': 1246.0,
            'visby': 1020.0},
        'bruges': {
            'antwerp': 58.4,
            'bergen': 559.0,
            'bremen': 320.0,
            'cologne': 208.0,
            'danzig': 901.0,
            'hamburg': 344.0,
            'kampen': 148.0,
            'london': 130.22,
            'lubeck': 749.0,
            'malmo': 642.0,
            'novorod': 1511.0,
            'riga': 1098.0,
            'rostock': 729.0,
            'stockholm': 1032.0,
            'stralsund': 718.0,
            'tallinn': 1155.0,
            'visby': 914.0},
        'bergen': {
            'antwerp': 667.0,
            'bruges': 559.0,
            'bremen': 480.0,
            'cologne': 658.0,
            'danzig': 726.0,
            'hamburg': 473.0,
            'kampen': 491.0,
            'london': 596.2,
            'lubeck': 568.0,
            'malmo': 466.0,
            'novorod': 1372.0,
            'riga': 953.0,
            'rostock': 556.0,
            'stockholm': 886.0,
            'stralsund': 541.0,
            'tallinn': 1009.0,
            'visby': 752.0},
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
            'antwerp': 935.6,
            'bruges': 901.0,
            'bergen': 726.0,
            'bremen': 751.0,
            'cologne': 999.0,
            'hamburg': 739.0,
            'kampen': 796.0,
            'london': 1089.21,
            'lubeck': 323.0,
            'malmo': 261.0,
            'novorod': 754.0,
            'riga': 328.0,
            'rostock': 277.0,
            'stockholm': 312.0,
            'stralsund': 245.0,
            'tallinn': 399.0,
            'visby': 210.0},
        'hamburg': {
            'antwerp': 372.6,
            'bruges': 344.0,
            'bergen': 473.0,
            'bremen': 116.0,
            'cologne': 446.0,
            'danzig': 739.0,
            'kampen': 231.0,
            'london': 420.85,
            'lubeck': 612.0,
            'malmo': 503.0,
            'novorod': 1354.0,
            'riga': 958.0,
            'rostock': 593.0,
            'stockholm': 884.0,
            'stralsund': 579.0,
            'tallinn': 1004.0,
            'visby': 777.0},
        'kampen': {
            'antwerp': 201.6,
            'bruges': 148.0,
            'bergen': 491.0,
            'bremen': 216.0,
            'cologne': 261.0,
            'danzig': 796.0,
            'hamburg': 231.0,
            'london': 257.0,
            'lubeck': 653.0,
            'malmo': 550.0,
            'novorod': 1395.0,
            'riga': 999.0,
            'rostock': 642.0,
            'stockholm': 910.0,
            'stralsund': 625.0,
            'tallinn': 1041.0,
            'visby': 813.0},
        'london': {
            'antwerp': 182.2,
            'bruges': 130.22,
            'bergen': 596.2,
            'bremen': 393.0,
            'cologne': 297.0,
            'danzig': 1089.21,
            'hamburg': 420.85,
            'kampen': 257.0,
            'lubeck': 835.0,
            'malmo': 710.05,
            'novorod': 1608.64,
            'riga': 1179.64,
            'rostock': 826.0,
            'stockholm': 790.0,
            'stralsund': 802.38,
            'tallinn': 1235.44,
            'visby': 993.3},
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
            'antwerp': 669.0,
            'bruges': 642.0,
            'bergen': 466.0,
            'bremen': 495.0,
            'cologne': 746.0,
            'danzig': 261.0,
            'hamburg': 503.0,
            'kampen': 550.0,
            'london': 710.1,
            'lubeck': 141.0,
            'novorod': 861.0,
            'riga': 453.0,
            'rostock': 97.7,
            'stockholm': 370.0,
            'stralsund': 83.0,
            'tallinn': 499.0,
            'visby': 269.0},
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
            'antwerp': 777.0,
            'bruges': 729.0,
            'bergen': 556.0,
            'bremen': 584.0,
            'cologne': 839.0,
            'danzig': 277.0,
            'hamburg': 593.0,
            'kampen': 642.0,
            'london': 826.0,
            'lubeck': 61.0,
            'malmo': 97.7,
            'novorod': 900.0,
            'riga': 498.0,
            'stockholm': 406.68088121782307,
            'stralsund': 57.526227214999764,
            'tallinn': 537.0273175055869,
            'visby': 306.74861339720417},
        'stockholm': {
            'antwerp': 1142.0,
            'bruges': 1032.0,
            'bergen': 886.0,
            'bremen': 864.0,
            'cologne': 1003.0,
            'danzig': 312.0,
            'hamburg': 884.0,
            'kampen': 910.0,
            'london': 790.0,
            'lubeck': 469.0,
            'malmo': 370.0,
            'novorod': 564.0,
            'riga': 240.0,
            'rostock': 406.68088121782307,
            'stralsund': 375.0,
            'tallinn': 206.0,
            'visby': 110.0},
        'stralsund': {
            'antwerp': 779.0,
            'bruges': 718.0,
            'bergen': 541.0,
            'bremen': 575.0,
            'cologne': 825.0,
            'danzig': 245.0,
            'hamburg': 579.0,
            'kampen': 625.0,
            'london': 802.4,
            'lubeck': 107.0,
            'malmo': 83.0,
            'novorod': 868.0,
            'riga': 467.0,
            'rostock': 57.526227214999764,
            'stockholm': 375.0,
            'tallinn': 503.0,
            'visby': 272.0},
        'tallinn': {
            'antwerp': 1246.0,
            'bruges': 1155.0,
            'bergen': 1009.0,
            'bremen': 995.0,
            'cologne': 1244.0,
            'danzig': 399.0,
            'hamburg': 1004.0,
            'kampen': 1041.0,
            'london': 1235.0,
            'lubeck': 598.0,
            'malmo': 499.0,
            'novorod': 371.0,
            'riga': 187.0,
            'rostock': 537.0273175055869,
            'stockholm': 206.0,
            'stralsund': 503.0,
            'visby': 239.0},
        'visby': {
            'antwerp': 1020.0,
            'bruges': 914.0,
            'bergen': 752.0,
            'bremen': 764.0,
            'cologne': 1014.0,
            'danzig': 210.0,
            'hamburg': 777.0,
            'kampen': 813.0,
            'london': 993.3,
            'lubeck': 365.0,
            'malmo': 269.0,
            'novorod': 600.0,
            'riga': 222.0,
            'rostock': 306.74861339720417,
            'stockholm': 110.0,
            'stralsund': 272.0,
            'tallinn': 239.0}}

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
