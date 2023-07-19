from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from scipy.stats import norm
from scipy.optimize import fsolve
from datetime import datetime, timedelta
import os


class TradeGoods(Enum):
    LINEN = 'linen'
    BROADCLOTH = 'broadcloth'
    CLOTHING = 'clothing'
    WOOD = 'wood'
    CHARCOAL = 'charcoal'
    PITCH = 'pitch'
    GRAIN = 'grain'
    HONEY = 'honey'
    HEMP = 'hemp'
    FLAX = 'flax'
    SPICES = 'spices'
    DYES = 'dyes'
    WINE = 'wine'
    MEAD = 'mead'
    BEER = 'beer'
    FISH = 'fish'
    OIL = 'oil'
    MEAT = 'meat'
    CHEESE = 'cheese'
    PELTS = 'pelts'
    WOOL = 'wool'
    IRON = 'iron'
    GEMS = 'gems'
    TOOLS = 'tools'
    WEAPONS = 'weapons'
    ARMOR = 'armor'
    JEWELRY = 'jewelry'
    FURNITURE = 'furniture'


class TradeGoodsCategory(Enum):
    TEXTILES = 'textiles'
    FORESTRY = 'forestry'
    FARMING = 'farming'
    ALCOHOL = 'alcohol'
    FISHING = 'fishing'
    RANCHING = 'ranching'
    MINING = 'mining'
    MANUFACTURED_ITEMS = 'manufactured_items'


class DemandLevel(Enum):
    ABSENT = auto()
    LOW = auto()
    REDUCED = auto()
    NORMAL = auto()
    ELEVATED = auto()
    HIGH = auto()
    EXTREME = auto()


class SupplyLevel(Enum):
    ABSENT = auto()
    LOW = auto()
    REDUCED = auto()
    NORMAL = auto()
    ELEVATED = auto()
    HIGH = auto()
    EXTREME = auto()


class Regions(Enum):
    ENGLISH_CHANNEL = "english channel"
    NORTH_SEA = "north sea"
    SOUTH_BALTIC = "south baltic"
    NORTH_BALTIC = "north baltic"


MARKET_EVENTS = {
    DemandLevel.EXTREME: [
        "In the  region, a new fashion trend has ignited a craze for  and . Demand for these textiles has hit unprecedented levels.",
        "The King's wedding in the  region has caused an extreme spike in the demand for jewelry, gems, wine, and luxury furniture.",
        "In Antwerp, a famous local artist's paintings have surged in popularity, driving up the demand for fine dyes and textiles to an all-time high.",
        "In London, the royal court has announced a grand feast. The demand for fine wines, cheese, meat, and exotic spices has skyrocketed."
    ],
    SupplyLevel.EXTREME: [
        "Exceptionally good weather and crop conditions in the  region has led to an extreme supply of , }.",
        "A large iron deposit was discovered in theesulting in a surge in the supply of iron, tools, weapons, and armor.",
        "Fishermen in Malmo have reported a bountiful season, resulting in an extreme supply of fish flooding the markets.",
        "Mines in Novgorod have struck a large vein of iron, leading to an extreme increase in the supply of iron and manufactured iron goods."
    ],
    DemandLevel.HIGH: [
        "Rising tensions on the s borders have led to a high demand for weapons, armor, and tools. Additionally, the region has seen a spike in the demand for mead and beer as soldiers look for ways to relax.",
        "The  region is preparing for a grand religious festival, leading to a high demand for spices, dyes, wine, and mead.",
        "With the construction of a new cathedral in Cologne, demand for wood, tools, and stained glass has risen dramatically.",
        "In Bremen, a trend of lavish parties among the nobility has led to a high demand for luxury goods, especially wine, spices, jewelry, and fine clothing."
    ],
    SupplyLevel.HIGH: [
        "Favorable fishing conditions in the  have led to an unusually high supply of fish and salt.",
        "An explosion in the bee population in the  region has resulted in a high supply of honey.",
        "Thanks to a bumper crop season in Riga, the supply of grain, flax, and hemp in the city's markets is at a high.",
        "The blacksmiths of Stockholm have perfected a new method of toolmaking, resulting in a surge of high-quality tools available."
    ],
    DemandLevel.ELEVATED: [
        "In the  region, an increase in construction projects has led to an elevated demand for wood, charcoal, pitch, and furniture.",
        "With the arrival of a travelling troupe in the , the demand for clothing, dyes, and alcohol has seen a notable increase.",
        "As Kampen gears up for its annual music festival, there's an elevated demand for honey and grain to produce mead and beer.",
        "The latest fashion trend in Bruges has caused an increase in demand for textiles such as linen and broadcloth."
    ],
    SupplyLevel.ELEVATED: [
        "A mild winter in the  region has led to an early and abundant harvest, providing an elevated supply of grain, flax, and hemp.",
        "The discovery of new pastures in the  region has led to an elevated supply of wool, pelts, meat, and cheese."
        "Excellent weather and ocean conditions have led to an elevated supply of fish in Bergen.",
        "Thanks to an unusually mild and wet summer, Stralsund has reported an elevated supply of honey."
    ],
    DemandLevel.NORMAL: [
        "Trade in the  region remains steady with a normal demand for forestry and manufactured items.",
        "In the  region, demand levels for farming and ranching products are normal and stable.",
        "Trade continues as usual in Tallinn with no significant change in demand for goods.",
        "Business as usual in Visby; demand for goods remains steady and normal."
    ],
    SupplyLevel.NORMAL: [
        "In the  region, supply of fishing and mining goods is steady, with no major changes in production reported.",
        "The region reports a normal supply of textiles and alcohol, as the production remains consistent.",
        "Hamburg's mines and workshops are working at their normal pace, and the supply of tools, weapons, and armor remains stable.",
        "Lubeck's forestry industry continues its steady production, keeping a normal supply of wood, charcoal, and pitch in the markets."
    ],
    DemandLevel.REDUCED: [
        "Due to a diplomatic dispute in the  region, the demand for luxury goods like gems, jewelry, and wine has reduced.",
        "A successful health campaign in the  region has led to reduced demand for alcohol and meat.",
        "Due to a recent grain surplus in Rostock, the demand for imported grain and related goods has been reduced.",
        "Following a peaceful treaty in Danzig, demand for weapons and armor has reduced significantly."
    ],
    SupplyLevel.REDUCED: [
        "The closure of several mines in the  region due to safety concerns has reduced the supply of iron, gems, and tools.",
        "A disease outbreak among livestock in the  region has led to a reduced supply of meat, cheese, pelts, and wool.",
        "A disease outbreak among the sheep flocks of Malmo has led to a reduced supply of wool, cheese, and meat.",
        "After a fire in one of the major workshops in London, the city sees a reduced supply of manufactured items."
    ],
    DemandLevel.LOW: [
        "Due to a religious fasting period in the  region, demand for meat, cheese, and alcohol is low.",
        "With the ongoing war in the  region, demand for non-essential manufactured items like furniture and jewelry is low.",
        "Following a period of fasting in Antwerp, demand for meat, fish, and cheese is currently low.",
        "With an economic downturn in Bremen, demand for luxury goods such as gems, jewelry, and fine furniture is low."
    ],
    SupplyLevel.LOW: [
        "Unfavorable weather conditions in the  region have resulted in a low supply of farming products like grain, flax, and hemp.",
        "A large forest fire in the  region has significantly reduced the supply of wood, charcoal, and pitch.",
        "Unfavorable weather conditions in Novgorod have led to a low supply of farming products.",
        "After an accident in one of the major mines in Tallinn, the city's supply of gems and iron is currently low."
    ],
    DemandLevel.ABSENT: [
        "A significant fish surplus in the {Regions} region has led to an absence of demand for imported fish.",
        "With the invention of synthetic fibers in the {Regions} region, the demand for natural textiles like linen and broadcloth is currently absent.",
        "Due to a fish surplus in Bergen, demand for imported fish is currently absent.",
        "Following a major scandal involving counterfeit gems in Visby, the demand for gems in the city has disappeared."
    ],
    SupplyLevel.ABSENT: [
        "Due to a severe blight, the {Regions} region reports an absence of grain supply.",
        "A major strike by miners in the {Regions} region has resulted in the complete absence of iron and gems supply.",
        "A plague of insects has devastated the grain crop in Stralsund. The city reports an absence of grain supply.",
        "A massive strike by workers in Hamburg's shipyards has halted production of wood, pitch, and tools."
    ]
}
MARKET_GOODS = {
    'linen': {'inputs': ['hemp', 'flax'], 'base_price': 10, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'textiles'},
    'broadcloth': {'inputs': ['wool', 'dyes'], 'base_price': 100, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'textiles'},
    'clothing': {'inputs': ['linen', 'wool', 'pelts', 'dyes'], 'base_price': 120, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'textiles'},
    'wood': {'inputs': [None], 'base_price': 30, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'forestry'},
    'charcoal': {'inputs': ['wood'], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'forestry'},
    'pitch': {'inputs': ['wood'], 'base_price': 80, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'forestry'},
    'grain': {'inputs': [None], 'base_price': 30, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'farming'},
    'honey': {'inputs': [None], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'farming'},
    'hemp': {'inputs': [None], 'base_price': 80, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'farming'},
    'flax': {'inputs': [None], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'farming'},
    'spices': {'inputs': [None], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'farming'},
    'dyes': {'inputs': [None], 'base_price': 120, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'farming'},
    'wine': {'inputs': [None], 'base_price': 150, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'alcohol'},
    'mead': {'inputs': ['honey'], 'base_price': 80, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'alcohol'},
    'beer': {'inputs': ['grain'], 'base_price': 60, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'alcohol'},
    'fish': {'inputs': ['salt'], 'base_price': 60, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'fishing'},
    'salt': {'inputs': [None], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'fishing'},
    'oil': {'inputs': ['fish'], 'base_price': 100, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'fishing'},
    'meat': {'inputs': ['salt'], 'base_price': 120, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'ranching'},
    'cheese': {'inputs': ['salt'], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'ranching'},
    'pelts': {'inputs': [None], 'base_price': 150, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'ranching'},
    'wool': {'inputs': [None], 'base_price': 90, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'ranching'},
    'iron': {'inputs': [None], 'base_price': 100, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'mining'},
    'gems': {'inputs': [None], 'base_price': 400, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'mining'},
    'tools': {'inputs': ['wood', 'iron', ], 'base_price': 150, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'manufactured_items'},
    'weapons': {'inputs': ['wood', 'iron', 'tools'], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'manufactured_items'},
    'armor': {'inputs': ['wood', 'iron', 'tools', 'clothing'], 'base_price': 300, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'manufactured_items'},
    'jewelry': {'inputs': ['iron', 'gems', 'tools'], 'base_price': 1000, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'manufactured_items'},
    'furniture': {'inputs': ['wood', 'linen', 'pelts', 'iron'], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': 'manufactured_items'}
}

CITIES = {
    'antwerp': {
        'region': 'english_channel',
        'distances': {
            'bruges': 58,
            'bergen': 667,
            'bremen': 397,
            'cologne': 283,
            'danzig': 936,
            'hamburg': 373,
            'kampen': 202,
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
        'productions': {
            'textiles': ['linen', 'clothing'],
            'farming': ['hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']
        }},
    'bruges': {
        'region': 'english_channel',
        'distances': {
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
        'productions': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'spices', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']
        }},
    'bergen': {
        'region': 'north_sea',
        'distances': {
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
        'productions': {
            'fishing': ['fish', 'oil'],
            'forestry': ['wood', 'charcoal', 'pitch']
        }},
    'bremen': {
        'region': 'north_sea',
        'distances': {
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
        'productions': {
            'alcohol': ['mead', 'beer', 'wine'],
            'ranching': ['pelts', 'wool', 'cheese'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey']
        }},
    'cologne': {
        'region': 'english_channel',
        'distances': {
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
        'productions': {
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey', 'spices'],
            'alcohol': ['wine', 'beer', 'mead']}},
    'danzig': {
        'region': 'south_baltic',
        'distances': {
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
        'productions': {
            'farming': ['grain', 'hemp', 'flax', 'honey'],
            'mining': ['iron', 'gems'], }
    },
    'hamburg': {
        'region': 'north_sea',
        'distances': {
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
        'productions': {
            'manufactured_items': ['jewelry', 'furniture'],
            'fishing': ['fish, oil, salt']
        }
    },
    'kampen': {
        'region': 'north_sea',
        'distances': {
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
        'productions': {
            'manufactured_items': ['jewelry', 'furniture'],
            'fishing': ['fish, oil, salt']}
    },
    'london': {
        'region': 'english_channel',
        'distances': {
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
        'productions': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey']},
    },
    'lubeck': {
        'region': 'south_baltic',
        'distances': {
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
        'productions': {
            'fishing': ['salt', 'fish', 'oil'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture']}
    },
    'malmo': {
        'region': 'south_baltic',
        'distances': {
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
        'productions': {
            'forestry': ['wood', 'charcoal', 'pitch'],
            'fishing': ['fish', 'oil', 'salt'],
            'manufactured_items': ['tools' 'weapons', 'armor']}
    },
    'novorod': {
        'region': 'north_baltic',
        'distances': {
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
        'productions': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems']}
    },
    'riga': {
        'region': 'north_baltic',
        'distances': {
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
        'productions': {
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
            'mining': ['iron', 'gems'],
            'forestry': ['wood', 'charcoal', 'pitch']},
    },
    'rostock': {
        'region': 'south_baltic',
        'distances': {
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
        'productions': {'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey'],
                        'ranching': ['meat', 'cheese', 'pelts', 'wool'],
                        'fishing': ['fish', 'salt']}
    },
    'stockholm': {
        'region': 'north_baltic',
        'distances': {
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
        'productions': {
            'mining': ['iron', 'gems'],
            'forestry': ['wood', 'charcoal', 'pitch']},
    },
    'stralsund': {
        'region': 'south_baltic',
        'distances': {
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
        'productions': {
            'textiles': ['linen', 'broadcloth', 'clothing'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'spices', 'honey'],
            'ranching': ['wool', 'pelts', 'cheese']}
    },
    'tallinn': {
        'region': 'north_baltic',
        'distances': {
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
        'productions': {
            'fishing': ['fish', 'oil'],
            'forestry': ['wood', 'charcoal', 'pitch']}
    },
    'visby': {
        'region': 'north_baltic',
        'distances': {
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
            'tallinn': 239},
        'productions': {
            'manufactured_items': ['tools', 'weapons', 'armor', 'jewelry', 'furniture'],
            'ranching': ['meat', 'cheese', 'pelts', 'wool'],
            'mining': ['iron', 'gems'],
            'farming': ['grain', 'hemp', 'flax', 'dyes', 'honey', 'spices'],
            'alcohol': ['wine', 'beer', 'mead']}}
}


@dataclass()
class MarketEvent:
    event_type: Enum
    affected_region: Enum
    affected_city: Enum
    affected_category: Enum
    affected_trade_good: Enum
    time_to_expire: datetime
    time_sent: datetime

    @classmethod
    def check_rumor(cls, city, item):
        # return list of events in a city
        pass

    @classmethod
    def check_MarketEvent(cls):
        # delete market event if days remaining is 0
        # call delete market event function
        pass

    @classmethod
    def delete_MarketEvent(cls, mktevent):
        pass

    @classmethod
    def get_market_rumor(cls, game):
        # excluding current player city, return a marketevent from a city or region
        pass

    @classmethod
    def create_MarketEvent(cls, city, rumor):
        # check all marketevents at given city,
        # create new marketevent with UUID in the cities that it applies to
        # if one market event of the same exact kind already exists, just extend its duration by that number of days
        pass


@dataclass()
class TravelModifier:
    # Travel Modifier used to modify travel times from city to city
    # applied to cities, and to players

    speed: float | None
    # pirates: bool | None
    # blockade: bool | None

    # speed is a % mod ranging from -50% to +50%
    @classmethod
    def set_travel_modifiers(cls, obj, travel_modifier: TravelModifier) -> None:
        mod_list = cls.get_travel_modifiers(obj)
        mod_list.append(travel_modifier)
        setattr(obj, 'travel_mod_list', mod_list)

    @classmethod
    def get_travel_modifiers(cls, obj) -> list[TravelModifier]:
        return getattr(obj, 'travel_mod_list')

    @classmethod
    def get_list_of_modifiers(cls, obj) -> list[TravelModifier]:
        return [getattr(obj, mods) for mods in obj.__dict__ if isinstance(getattr(obj, mods), TravelModifier)]


@dataclass(kw_only=True)
class Item:
    # base item class used for handling construction of all trading goods
    # Used critically in the construction of the Inventory base classes
    item_name: str
    quantity: int
    category: str
    inputs: list[str]

    def get_item_name(self) -> str:
        return self.item_name

    def get_item_quantity(self) -> int:
        return getattr(self, 'quantity')

    def set_item_quantity(self, new_value) -> None:
        setattr(self, 'quantity', new_value)

    def get_item_category(self) -> str:
        return self.category

    def get_item_inputs(self) -> list[str]:
        return self.inputs


@dataclass()
class PlayerItem(Item):
    last_seen_price: int = 0
    last_purchase_price: int = 0
    last_purchase_quantity: int = 0
    last_seen_demand: DemandLevel = DemandLevel.NORMAL
    last_sale_price: int = 0
    last_sale_quantity: int = 0

    def set_last_seen_demand(self, demand: DemandLevel):
        self.last_seen_demand = demand

    def set_last_seen_price(self, price):
        self.last_seen_price = price

    def set_last_purchase_price(self, price):
        self.last_purchase_price = price

    def set_last_purchase_quantity(self, quantity):
        self.last_purchase_quantity = quantity

    def set_last_sale_price(self, price):
        self.last_sale_price = price

    def set_last_sale_quantity(self, quantity):
        self.last_purchase_price = quantity


@dataclass()
class MarketItem(Item):

    price: int = 0
    demand: DemandLevel = DemandLevel.NORMAL
    supply: SupplyLevel = SupplyLevel.NORMAL
    previous_price: int = 0
    previous_quantity: int = 0
    previous_day_demand: DemandLevel = DemandLevel.NORMAL
    previous_day_supply: SupplyLevel = SupplyLevel.NORMAL

    def __post_init__(self):
        self.demand_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.demand_mu = MARKET_GOODS[self.item_name]['base_price'] / 2
        self.supply_sigma = MARKET_GOODS[self.item_name]['base_price'] / 4
        self.supply_mu = MARKET_GOODS[self.item_name]['base_price'] / 2

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price

    def set_previous_price(self, val):
        self.previous_price = val

    def set_previous_quantity(self, val):
        self.previous_quantity = val

    def set_demand_mu(self, val):
        setattr(self, 'demand_mu', val)

    def get_demand_mu(self):
        return getattr(self, 'demand_mu')

    def set_supply_mu(self, val):
        setattr(self, 'supply_mu', val)

    def get_supply_mu(self):
        return getattr(self, 'supply_mu')

    def set_demand_sigma(self, val):
        setattr(self, 'demand_sigma', val)

    def get_demand_sigma(self):
        return getattr(self, 'demand_sigma')

    def set_supply_sigma(self, val):
        setattr(self, 'supply_sigma', val)

    def get_supply_sigma(self):
        return getattr(self, 'supply_sigma')


@dataclass()
class Inventory:
    # base inventory class used to define goods

    def get_item(self, item: str) -> Item:
        return getattr(self, item)

    def get_list_of_items(self) -> list[Item]:
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem) or isinstance(getattr(self, items), MarketItem)]

    def has_input(self, trade_good: str) -> list[Item]:
        return [item for item in self.get_list_of_items(
        ) if trade_good in item.inputs]

    def has_category(self, trade_good_category: str) -> list[Item]:
        return [item for item in self.get_list_of_items() if item.category is trade_good_category]


@dataclass(kw_only=True)
class PlayerInventory(Inventory):
    # inventory-like object for a player, inherits from Inventory

    def __init__(self) -> None:
        self.gold = 1000
        for item, info in MARKET_GOODS.items():
            trade_good = PlayerItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_player_item(self, item: str) -> PlayerItem:
        return getattr(self, item)

    def get_gold(self) -> int:
        return self.gold

    def set_gold(self, new_gold) -> None:
        self.gold = new_gold

    def get_capacity(self) -> int:
        return self.capacity

    def set_capacity(self, new_capacity) -> None:
        self.capacity = new_capacity

    def get_list_of_items(self) -> list[PlayerItem]:
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem) or isinstance(getattr(self, items), MarketItem)]

    def get_current_inventory(self) -> dict[str, dict[str, int]]:
        current_inv = {}
        for item in self.get_list_of_items():
            name = item.get_item_name()
            quantity = item.get_item_quantity()
            cost = item.last_purchase_price
            current_inv[name] = {'quantity': quantity, 'cost': cost}
        return current_inv


@dataclass(kw_only=True)
class Market(Inventory):
    # inventory-like object for use within a City object in game structure

    def __init__(self) -> None:
        for item, info in MARKET_GOODS.items():
            trade_good = MarketItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_market_item(self, item: str) -> MarketItem:
        return getattr(self, item)

    def get_list_of_items(self) -> list[MarketItem]:
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem) or isinstance(getattr(self, items), MarketItem)]

    def get_market_data(self):
        market_info = list()
        for item in self.get_list_of_items():
            market_info.append(
                [item.get_item_name(), item.get_price(), item.get_item_quantity()])
        return market_info


@dataclass
class View:

    # handles all GUI aspects of game
    def __init__(self, game: Game) -> None:
        self.game = game
        self.menu_selection = None
        self.menu = ['Trade', 'Trave', 'Inventory', 'Quit']

    def game_loop(self):

        os.system('clear' if os.name == 'posix' else 'cls')
        while True:

            self.clear_sceen()
            self.print_game_status()
            self.game_menu()

            # self.process_input()

            if self.menu_selection == self.menu[3]:
                break

            self.game.advance_days(1)

    def clear_sceen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def get_datetime(self):
        return self.game.current_date

    def get_player_location(self):
        return self.game.player.get_player_location()

    def print_game_status(self):
        print(
            f"Day: {self.get_datetime()} Location: {self.get_player_location()}")

        # print("Last Action:", self.user_last_action)
        # print(self.player.show_inventory())
        print("Gold:", self.game.player.inv.get_gold())

    def print_player_inventory(self):
        player_items: dict[str, dict[str, int]
                           ] = self.game.player.inv.get_current_inventory()
        print("Player Inventory")
        for item, info in player_items.items():
            quantity: int | None = info.get('quantity')
            cost: int | None = info.get('cost')
            if info.get('quantity'):
                print(f"Items:{item} Quantity:{quantity} Cost:{cost}")

    def game_menu(self, statement=None):
        if statement:
            print(statement)
        print("What would you like to do?")
        for i, option in enumerate(self.menu):
            print(f"{i+1}. {option}")
        choice = int(input("Enter the number of your choice: "))
        # Validators.range_of_list(choice, self.menu, self.game_menu)
        self.menu_selection = [choice - 1]
        # self.menu_selection = choice - 1


class Travel:
    # Module handles travel between Cities
    nautical_miles_per_hour = 6

    @classmethod
    def get_time_to_travel(cls, player: Player, origin: City, destination: City):
        travel_time: timedelta
        origin_name = origin.get_location_name()
        destination_name = destination.get_location_name()
        modlist = []
        # lookup distance
        if CITIES[origin_name].get('distances'):
            distances = CITIES[origin_name].get('distances')
            if distances.get(destination_name):
                destination_distance = distances.get(destination_name)
            else:
                UnboundLocalError()
        else:
            UnboundLocalError()

        # check player state for upgrades
        if TravelModifier.get_travel_modifiers(player):
            for mod in TravelModifier.get_travel_modifiers(player):
                modlist.append(mod)
                print(mod)
        if TravelModifier.get_travel_modifiers(origin):
            for mod in TravelModifier.get_travel_modifiers(origin):
                modlist.append(mod)
                print(mod)
        if TravelModifier.get_travel_modifiers(destination):
            for mod in TravelModifier.get_travel_modifiers(destination):
                modlist.append(mod)
                print(mod)

        total_percentage = 1
        for mod in modlist:
            total_percentage += mod.speed
        # sum modlist

        # randomize the travel time
        speed = total_percentage * cls.nautical_miles_per_hour
        time_to_travel = destination_distance / speed

        deltatime = timedelta(hours=time_to_travel)

        return deltatime

    # @classmethod
    # def calc_travel_speed(cls, distance, modifier) -> float:
    #     pass


@dataclass()
class Player:
    # constructor player object
    name: str
    location: City
    travel_mod_list: list
    inv: PlayerInventory = field(default_factory=PlayerInventory)

    def get_player_location(self):
        return self.location


@dataclass()
class City:
    # city object contains
    # Market object
    # Market inherits Inventory contains Items
    name: str
    travel_mod_list: list
    market: Market = field(default_factory=Market)

    def get_location_name(self) -> str:
        return self.name

    def sort_closest_cities(self, citylist=CITIES):
        citylist_copy = citylist[self.name]['distances'].copy()
        citylist_copy = dict(sorted(citylist_copy.items(), key=lambda x: x[1]))
        return citylist_copy


class Economy:
    # Market pricing mechanics
    # sets demands, initial supply
    # updates economy as

    @classmethod
    def update_market(cls, city):
        for item in city.market.get_list_of_items():
            cls.update_pricing(item)

    @classmethod
    def update_pricing(cls, item):
        # class method to update individual item pricing at a market
        demand_mu = item.get_demand_mu()
        demand_sigma = item.get_demand_sigma()
        supply_mu = item.get_supply_mu()
        supply_sigma = item.get_supply_sigma()
        old_price = item.get_price()
        old_qty = 100
        item.set_previous_price(old_price)
        item.set_previous_quantity(old_qty)

        def demand(p, mu, sigma):
            return norm.sf(p, mu, sigma)

        def supply(p, mu, sigma):
            return norm.cdf(p, mu, sigma)

        def find_equilibrium(demand_mu, demand_sigma, supply_mu, supply_sigma):
            price_eq = fsolve(lambda p: supply(
                p, supply_mu, supply_sigma) - demand(p, demand_mu, demand_sigma), 0.5)
            quantity_eq = supply(price_eq, supply_mu, supply_sigma)

            # returns a tuple representing the given coordinates price(gold) and quantity(% of total city demand/production) that solves for the two functions of supply and demand
            coordinates = (price_eq[0], quantity_eq[0])
            return coordinates

        output = find_equilibrium(
            demand_mu, demand_sigma, supply_mu, supply_sigma)

        new_price = round(output[0])
        new_qty = round(output[1] * old_qty)

        item.set_item_quantity(new_qty)
        item.set_price(new_price)

    @classmethod
    def update_supply(cls, city, item):
        # previous_supply = city.market.item.get_supply()
        # price = city.market.item.get_price()
        # demand = city.market.item.get_demand()
        pass

    @classmethod
    def update_demand(cls, city, item):
        # previous_demand = city.market.item.get_demand()
        # price = city.market.item.get_price()
        # supply = city.market.item.get_supply()
        pass


@dataclass()
class Game:
    current_date = datetime(year=1393, month=7, day=29, hour=8, minute=0)
    player: Player
    # all game logic ends up in here

    def __init__(self, player_name='Michael', starting_city='lubeck') -> None:
        # setup all game objects at setattr
        self.player_name = player_name
        self.build_cities()
        self.update_city_inventories()
        self.starting_city = starting_city
        self.player = self.create_player()

    def advance_days(self, days_to_advance):
        self.current_date += timedelta(days=days_to_advance)

    def build_cities(self) -> None:
        for city in CITIES.keys():
            new_city = City(city, market=Market(), travel_mod_list=[])
            setattr(self, city, new_city)

    def create_player(self) -> Player:
        city = self.get_city(self.starting_city)
        return Player(self.player_name, city, travel_mod_list=[])

    def list_of_players(self):
        return getattr(self, 'player')

    def list_of_cities(self):
        return [city for city in dir(self) if isinstance(getattr(self, city), City)]

    def get_city(self, city: str) -> City:
        return getattr(self, city)

    def update_city_inventories(self) -> None:
        # for city in self.list_of_cities():
        #     Economy.update_supply(city)
        #     Economy.update_demand(city)
        #     Economy.update_pricing(city)
        pass

    def build_rumors(self):
        pass


def main():
    app = Game()
    for city in app.list_of_cities():
        lookupcity = app.get_city(city)
        Economy.update_market(lookupcity)

    # for city in app.list_of_cities():
    #     lookupcity = app.get_city(city)
    #     print(lookupcity.market.get_market_data())
    # view.print_game_status()
    # view.print_player_inventory()
    # app.advance_days(2098)
    print(Travel.get_time_to_travel(
        app.player, app.player.location, app.get_city('hamburg')))

    # view.print_game_status()
    TravelModifier.set_travel_modifiers(app.get_city('hamburg'), neg_fifty)

    print(Travel.get_time_to_travel(
        app.player, app.player.location, app.get_city('hamburg')))

    print(Travel.get_time_to_travel(
        app.player, app.player.location, app.get_city('antwerp')))

    print(Travel.get_time_to_travel(
        app.player, app.player.location, app.get_city('novorod')))


if __name__ == "__main__":
    main()
