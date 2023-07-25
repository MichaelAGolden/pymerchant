from __future__ import annotations
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from scipy.optimize import fsolve
from scipy.stats import norm
from rich import print
from rich.panel import Panel
from helper import range_of_list


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


# MARKET_EVENTS is a dictionary of DemandLevel and SupplyLevel events that affect the a given region, city, or market_good.
MARKET_EVENTS: dict[DemandLevel | SupplyLevel, list[str]] = {

    DemandLevel.EXTREME: [
        "In the region, a new fashion trend has ignited a craze for  and . Demand for these textiles has hit unprecedented levels.",
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


@dataclass(kw_only=True)
class Item:
    """
    Class that describes an Item or "TradeGood", super class to PlayerItem and MarketItem
    """
    item_name: str
    quantity: int
    category: str
    inputs: list[str]


@dataclass()
class PlayerItem(Item):
    """
    Class that describes a PlayerItem object, inherits from Item

    """
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


@dataclass()
class Inventory:
    """
    Class that describes an Inventory object, super class to PlayerInventory and MarketInventory
    """

    def get_list_of_items(self) -> list[Item]:
        """
        Returns list of items in inventory

        Returns:
            list[Item]: list of Item objects
        """
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem) or isinstance(getattr(self, items), MarketItem)]

    def has_input(self, trade_good: str) -> list[Item]:
        """
        Returns list of items that have inputs of a given trade_good

        Args:
            trade_good (str): TradeGood

        Returns:
            list[Item]: List of Item objects
        """
        return [item for item in self.get_list_of_items(
        ) if trade_good in item.inputs]

    def has_category(self, trade_good_category: str) -> list[Item]:
        """
        Returns list of items that have a specific trade_good_category

        Args:
            trade_good_category (str): TradeGoodsCategory

        Returns:
            list[Item]: List of Item objects
        """
        return [item for item in self.get_list_of_items() if item.category is trade_good_category]


@dataclass(kw_only=True)
class PlayerInventory(Inventory):
    """
    Class that describes a PlayerInventory object, inherits from Inventory

    """

    def __init__(self) -> None:
        """
        Initializes PlayerInventory
        """
        self.gold = 1000
        for item, info in MARKET_GOODS.items():
            trade_good = PlayerItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_player_item(self, item: str) -> PlayerItem:
        """
        Returns player_item via an accessor method.

        While not traditionally "pythonic" this prevents runtime errors if an item attribute is not a keyword property of the PlayerInventory

        Args:
            item (str): item name to lookup

        Returns:
            PlayerItem: The PlayerItem object
        """
        return getattr(self, item)

    def get_list_of_items(self) -> list[PlayerItem]:
        """
        Returns list of items of PlayerItem type in PlayerInventory

        Returns:
            list[PlayerItem]: PlayerItem Objects
        """
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem)]

    def get_current_inventory(self) -> dict[str, dict[str, int]]:
        """
        Returns a dictionary within a dictionary of items in inventory with their quanity and cost as a values to their named keys

        Returns:
            dict[str, dict[str, int]]: dict[name: item_name, {'quantity':item.quantity, 'cost': item.cost}]
        """
        current_inv = {}
        for item in self.get_list_of_items():
            name = item.item_name
            quantity = item.quantity
            cost = item.last_purchase_price
            current_inv[name] = {'quantity': quantity, 'cost': cost}
        return current_inv


@dataclass(kw_only=True)
class Market(Inventory):
    """
    Class that describes an MarketInventory object, inherits from Inventory class
    """

    def __init__(self) -> None:
        """
        Initializes MarketInventory
        """
        for item, info in MARKET_GOODS.items():
            trade_good = MarketItem(item_name=item, quantity=0,
                                    category=info['category'], inputs=info['inputs'])
            setattr(self, item, trade_good)

    def get_list_of_items(self) -> list[MarketItem]:
        """
        Returns list of MarketItems in MarketInventory

        Returns:
            list[MarketItem]: MarketItem object
        """
        return [getattr(self, items) for items in self.__dict__ if isinstance(getattr(self, items), Item) or isinstance(getattr(self, items), PlayerItem) or isinstance(getattr(self, items), MarketItem)]

    def get_market_data(self):
        """
        Returns a list of list of [item_name, item.price, item.quantity] for all items in market

        Returns:
            list[list[str,int,int]]: [[self.item_name, self.item.price, self.item.quantity]...[]]
        """
        market_info = list()
        for item in self.get_list_of_items():
            market_info.append(
                [item.item_name, item.price, item.quantity])
        return market_info

    @classmethod
    def update_market(cls, city):
        """
        Updates all prices for items in a given city

        Args:
            city (City): City we are updating
        """
        for item in city.market.get_list_of_items():
            cls.update_pricing(item)

    @classmethod
    def update_pricing(cls, item: MarketItem):
        """
        needs rework
        Args:
            item (MarketItem): _description_

        Returns:
            _type_: _description_
        """

        # class method to update individual item pricing at a market
        demand_mu = item.demand_mu
        demand_sigma = item.demand_sigma
        supply_mu = item.supply_mu
        supply_sigma = item.supply_sigma

        item.previous_price = item.price
        item.previous_quantity = item.quantity

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
        new_qty = round(output[1] * item.previous_quantity)

        item.quantity = new_qty
        item.price = new_price

    @classmethod
    def update_supply(cls, city, item):
        # previous_supply = city.market.item.get_supply()
        # price = city.market.item.price
        # demand = city.market.item.get_demand()
        pass

    @classmethod
    def update_demand(cls, city, item):
        # previous_demand = city.market.item.get_demand()
        # price = city.market.item.price()
        # supply = city.market.item.get_supply()
        pass


@dataclass()
class MarketEvent:
    """
    MarketEvent()

    event_type: Supply(shock) | Demand(shock)
    affected_region: None | Region that is affected refer to class Regions(enum)
    affected_city: City affected (required) - Market Events are assigned at City level, cannot be populated to region alone
    affected_category: TradeGoodsCategory | None - Good category if specified
    affected_trade_good: TradeGoods | None - Trade good specifically affected
    time_to_expire: datetime.timedelta - to be used to set a specific time expiry
    time_sent: datetime - record of when MarketEvent object created, (may delete)

    Describes a MarketEvent object
    These are events that affect supply and demand for goods across the world
    They are generated by the game every turn at random and generally can be thought of as following a gaussian distribution in their affect and occurance

    Meaning "extreme" events are much less likely than "elevated" events and are even even less likely than "normal" events. There are 7 levels of events that you can think of as std deviations away from the mean (normal) 3 deviations above and 3 below

    class also features the relevant classmethods
    """
    event_type: Enum
    affected_region: Enum
    affected_city: Enum
    affected_category: Enum
    affected_trade_good: Enum
    time_to_expire: datetime
    time_sent: datetime

    @classmethod
    def get_MarketEvent(cls, city: City, item: MarketItem):
        """
        Returns list of MarketEvent() objects for a given city, item pair
        Allows lookup of specific events with regards to specific items in specific cities
        Args:
            city (City): City that you are looking for checking for a MarketEvent
            item (MarketItem(item)): Item or TradeGood that you are checking for an applicable MarketEvent

        Returns:
            list[MarketEvent]: All MarketEvent objects for a given city, item pair
        """
        [getattr(city, event) for event in city.__dict__ if isinstance(
            getattr(city, event), MarketEvent)]

    @classmethod
    def check_MarketEvent(cls, city: City):
        """
        Checks and resolves all MarketEvents in a given city, deleting any events at or beyond expiry

        Args:
            event (MarketEvent): The kMarketEvent to be deleted
        Calls:
            delete_MarketEvent(city)
        Returns:
            None
        """
        for event in cls.get_all_events(city):
            if event.time_to_expire <= Game.current_date:
                cls.delete_MarketEvent(event)

    @classmethod
    def delete_MarketEvent(cls, event: MarketEvent):
        """
        Deletes MarketEvent from city attributes when called

        Args:
            event (MarketEvent): MarketEvent obj to be deleted
        """
        delattr(event.affected_city, event.__repr__())

    @classmethod
    def get_all_events(cls, city: City):
        """
        Returns list of MarketEvents in a city when called

        Args:
            city (City): City MarketEvent are in city attributes at time of call

        Returns:
            List[MarketEvent]: List of all MarketEvent objects
        """
        return [getattr(city, events) for events in city.__dict__ if isinstance(getattr(city, events), MarketEvent)]

    @classmethod
    def create_MarketEvent(cls, city: City, event):
        """
        Placeholder - working on UUID system for marketevents, MarketEvent Generator

        Args:
            city (_type_): _description_
            rumor (_type_): _description_
        """
        pass


@dataclass()
class TravelModifier:
    """
    Describes a TravelModifier object, modifies travel speed and thereby time to arrival in a city. This can affect whether or not a player can arrive in time before a MarketEvent expires changing pricing and available good quantities.
    """

    speed: float | None
    # pirates: bool | None
    # blockade: bool | None

    # speed is a % mod ranging from -50% to +50%
    @classmethod
    def set_travel_modifiers(cls, obj: Player | City, travel_modifier: TravelModifier) -> None:
        """
        Sets or appends TravelModifier Objects to Player | City  objects current TravelModifiers as called by get_travel_modifiers(obj)

        Args:
            obj (Any): Player | City
            travel_modifier (TravelModifier): TravelModifier object to append to obj

        Calls:
            cls.get_travel_modifiers(obj): Returns list of TravelModifier

        Returns:
            None
        """
        mod_list = cls.get_travel_modifiers(obj)
        mod_list.append(travel_modifier)
        setattr(obj, 'travel_mod_list', mod_list)

    @classmethod
    def get_travel_modifiers(cls, obj: Player | City) -> list[TravelModifier]:
        """
        Returns list of TravlelModifier objects for a given object at time of method call

        Args:
            obj (Any): Player | City affected by a TravelModifier

        Returns:
            list[TravelModifier]: list of all TravelModifier applying to Player | City
        """
        return getattr(obj, 'travel_mod_list')

    # @classmethod
    # def get_list_of_modifiers(cls, obj) -> list[TravelModifier]:
    #     """
    #     Returns list of TravelModifier objects for a given obj: Any

    #     These are the negative or positive affects on travel speed
    #     Args:
    #         obj (Player | City ): Object that is modified

    #     Returns:
    #         list[TravelModifier]: List of TravelModifier
    #     """
    #     return [getattr(obj, mods) for mods in obj.__dict__ if isinstance(getattr(obj, mods), TravelModifier)]


@dataclass()
class Player:
    """
    Describes Player object
    Player does have access to the City object the player is located in
    Player also has access to their PlayerInventory

    Care is needed to not inadvertently call a cities inventory self.location.market instead of self.inv
    """
    name: str
    location: City
    travel_mod_list: list
    travel_speed = nautical_miles_per_hour = 6
    inv: PlayerInventory = field(default_factory=PlayerInventory)

    @classmethod
    def get_time_to_travel(cls, player: Player, origin: City, destination: City):
        travel_time: timedelta
        origin_name = origin.name
        destination_name = destination.name
        modlist = []
        # lookup distance
        if CITIES[origin_name].get('distances'):
            distances = CITIES[origin_name].get('distances')
            try:
                if distances.get(destination_name):
                    destination_distance = distances.get(destination_name)
            except:
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


@dataclass()
class City:
    """
    Describes City Object
    """
    name: str
    travel_mod_list: list
    market: Market = field(default_factory=Market)

    def sort_closest_cities(self, citylist=CITIES) -> dict[str, int]:
        """
        Sorting function for cities by distance.

        Note: Each distance in the CITIES dictionary was measured by hand from city to city in Google Earth in Nautical Miles by a novice approximation of a sea route.
        Likely these numbers are far off what real maritime sailing distance approximations would be, but I did not have the experience or time to write a program to approximate these distances for me, and from my research, it seems that if you could write such a program, it could be a very lucrative endeavor as the paid programs for this are very expensive.

        Nevertheless, these approximations are much more accurate than a as the crow flies measure between cities.

        Args:
            citylist (dict[str: dict[str, Any]]): Dictionary of cities with their coorresponding production attributes, used to build City objects. Defaults to CITIES.

        Returns:
            dict[str, int]: _description_
        """
        citylist_copy = citylist[self.name]['distances'].copy()
        citylist_copy = dict(sorted(citylist_copy.items(), key=lambda x: x[1]))
        return citylist_copy


@dataclass()
class Game:
    """
    Game class holds all objects necessary for the game, including Player, City, and all of their objects and attriburtes

    Game logic and initialization of game occurs here
    """
    current_date = datetime(year=1393, month=7, day=29, hour=8, minute=0)
    player: Player

    def __init__(self, player_name='Michael', starting_city='lubeck') -> None:
        """
        Games

        Args:
            player_name (str, optional): Name of Player. Defaults to 'Michael'.
            starting_city (str, optional): Name of starting_city player is located in. Defaults to 'lubeck'.
        """
        self.player_name = player_name
        self.build_cities()
        self.update_city_inventories()
        self.starting_city = starting_city
        self.player = self.create_player()

    def advance_days(self, time: timedelta):
        """
        Advances game time by a datetime.timedelta

        Args:
            time (timedelta): timedelta is defined in datetime module
        """
        self.current_date += time

    def build_cities(self) -> None:
        """
        Creates all city objects for game and assigns them to our game object

        To be run in __init__() function

        Note we use setattr() function because cities are not defined as keyword properties at time of
        """
        for city in CITIES.keys():
            new_city = City(city, market=Market(), travel_mod_list=list())
            setattr(self, city, new_city)

    def create_player(self) -> Player:
        """
        Creates player object for game

        Returns:
            Player: Player object
        """
        city = self.get_city(self.starting_city)
        return Player(self.player_name, city, travel_mod_list=[])

    def list_of_cities(self):
        """
        Returns list of cities in game

        Returns:
            List[City]: List of City objects in game
        """
        return [city for city in dir(self) if isinstance(getattr(self, city), City)]

    def get_city(self, city: str) -> City:
        """
        Returns player_item via an accessor method.

        While not traditionally "pythonic" this prevents runtime errors if a City object is not an attribute of the Game

        Args:
            city (str): Name of city, not the City object itself

        Returns:
            City: City Object
        """
        return getattr(self, city)

    def update_city_inventories(self) -> None:
        """
        Function to update inventory supply level and pricing for all cities in the game, to be run ONLY once per game day
        """
        # for city in self.list_of_cities():
        #     Economy.update_supply(city)
        #     Economy.update_demand(city)
        #     Economy.update_pricing(city)
        pass


@dataclass
class View:
    """
    View component of the game, wraps around game object.

    This could be later replaced by a more complex system written in CURSES or some non-console based game.
    I've considered adding a GUI but that might be too much for this time
    """
    game: Game

    def __init__(self) -> None:
        """
        Initializes View object, defines menu and keyword attributes not set in @dataclass() init
        """
        self.game = Game()
        self.menu = ['Travel', 'Trade', 'Inventory', 'Quit']
        self.menu_selection = None
        self.user_last_action = None
        self.time_passed = None

    def game_loop(self):
        """
        Main loop that runs and draws the screen and calls the relevant functions in from view and game
        """
        while self.menu_selection != 'Quit':
            Market.update_market(self.game.player.location)
            self.game_menu()
            self.process_input()

    def clear_sceen(self):
        """
        Function that clears screen depending on what OS user is running
        """
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_game_status(self):
        """
        Simple game status method intended to be called at start of each turn or menu selection
        """
        print(Panel.fit("[bold yellow] Hi, I'm a Panel", border_style="red"))
        print(
            f"Date: {self.game.current_date} Location: {self.game.player.location.name.capitalize()}")
        print("Time Passed:", self.time_passed)
        print("Last Action:", self.user_last_action)
        print("Gold:", self.game.player.inv.gold)

    def print_player_inventory(self):
        """
        Prints a formatted list of non-zero quantity player inventory items
        """
        player_items: dict[str, dict[str, int]
                           ] = self.game.player.inv.get_current_inventory()
        hyphen = chr(45)

        print(f"{'Player Inventory':{hyphen}^60}")
        print(f"{'Trade Good':<20}{'Quantity':>20}{'Cost':^20}")
        for item, info in player_items.items():
            quantity: int | None = info.get('quantity')
            cost: int | None = info.get('cost')
            if info.get('quantity'):
                print(f"Items:{item} Quantity:{quantity} Cost:{cost}")

    def game_menu(self):
        """
        Displays game_menu and asks user for input

        """
        self.clear_sceen()
        self.print_game_status()

        print("What would you like to do?")

        for i, option in enumerate(self.menu):
            print(f"{i+1}. {option}")

        choice = range_of_list(self.menu)

        self.menu_selection = self.menu[choice - 1]

    def travel(self):
        self.clear_sceen()
        self.print_game_status()

        enumerate_city_dist = enumerate(self.game.player.location.sort_closest_cities(
        ).items())

        list_of_cities = []

        for i, (city, distance) in enumerate_city_dist:
            print(f"{i+1}. {city} {distance} (distance in NM)")
            list_of_cities.append((city, distance))

        choice = range_of_list(list_of_cities)

        new_location = list_of_cities[choice - 1][0]

        self.time_passed = Player.get_time_to_travel(
            self.game.player, self.game.player.location, self.game.get_city(new_location))
        self.game.current_date += self.time_passed
        self.game.player.location = self.game.get_city(new_location)
        print(
            f"You have arrived in {self.game.player.location.name.capitalize()}.")

    def trade(self):
        self.print_game_status()

        item_list = self.game.player.location.market.get_market_data()

        # Build table for displaying trade - refactor into a function
        for idx, item in enumerate(item_list):
            print(
                f"{idx+1}) --{item[0]}--|-----{item[1]}-----|------{item[2]}-------")

        # Get User Input - refactor into other functions?
        user_item_choice = int(
            input("Enter the number cooresponding to the item: "))

        user_item_qty = int(input("How many would you like to buy? "))

        # Variable assignment
        item_price = item_list[user_item_choice - 1][1]
        user_item_cost = user_item_qty * item_price
        user_item_name = item_list[user_item_choice - 1][0]

        delta = timedelta(hours=1)
        self.game.current_date += delta
        # self.player.buy_update_inventory(
        #     user_item_name, user_item_qty, item_price, user_item_cost)

    def show_inventory(self):
        self.clear_sceen()
        self.print_game_status()
        self.print_player_inventory()

        exit_inventory = False
        while not exit_inventory:
            exit_inventory = input("Press any key to exit inventory")

    def process_input(self):
        if self.menu_selection == self.menu[0]:
            self.user_last_action = "Travel"
            self.travel()
        elif self.menu_selection == self.menu[1]:
            self.user_last_action = "Trade"
            self.trade()
        elif self.menu_selection == self.menu[2]:
            self.user_last_action = "Inventory"
            self.show_inventory()
        elif self.menu_selection == self.menu[3]:
            self.user_last_action = "Quit"
            print(self.user_last_action)
        else:
            print("Invalid input.")


def main():
    console = View()
    console.game_loop()


if __name__ == "__main__":
    main()
