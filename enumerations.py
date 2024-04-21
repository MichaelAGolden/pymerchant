from enum import StrEnum, Enum, auto


class TradeGoods(StrEnum):
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
    SALT = 'salt'
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


class TradeGoodsCategory(StrEnum):
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


class Region(StrEnum):
    ENGLISH_CHANNEL = "English Channel"
    NORTH_SEA = "North Sea"
    SOUTH_BALTIC = "South Baltic"
    NORTH_BALTIC = "North Baltic"


# MARKET_EVENTS is a dictionary of DemandLevel and SupplyLevel events that affect the a given region, city, or market_good. - WIP
# MARKET_EVENTS: dict[DemandLevel | SupplyLevel, list[str]] = {

#     DemandLevel.EXTREME: [

#     ],
#     SupplyLevel.EXTREME: [

#     ],
#     DemandLevel.HIGH: [

#     ],
#     SupplyLevel.HIGH: [

#     ],
#     DemandLevel.ELEVATED: [

#     ],
#     SupplyLevel.ELEVATED: [

#     ],
#     DemandLevel.NORMAL: [

#     ],
#     SupplyLevel.NORMAL: [

#     ],
#     DemandLevel.REDUCED: [

#     ],
#     SupplyLevel.REDUCED: [

#     ],
#     DemandLevel.LOW: [

#     ],
#     SupplyLevel.LOW: [

#     ],
#     DemandLevel.ABSENT: [

#     ],
#     SupplyLevel.ABSENT: [

#     ]}

MARKET_GOODS = {
    TradeGoods.LINEN: {'inputs': [TradeGoods.HEMP, TradeGoods.FLAX], 'mu': 22, 'sigma': 4, 'category': TradeGoodsCategory.TEXTILES},
    TradeGoods.BROADCLOTH: {'inputs': [TradeGoods.WOOL, TradeGoods.DYES], 'mu': 100, 'sigma': 22, 'category': TradeGoodsCategory.TEXTILES},
    TradeGoods.CLOTHING: {'inputs': [TradeGoods.LINEN, TradeGoods.WOOL, TradeGoods.PELTS, TradeGoods.DYES], 'mu': 240, 'sigma': 35, 'category': TradeGoodsCategory.TEXTILES},

    TradeGoods.WOOD: {'inputs': [None], 'mu': 30, 'sigma': 7, 'category': TradeGoodsCategory.FORESTRY},
    TradeGoods.CHARCOAL: {'inputs': [TradeGoods.WOOD], 'mu': 50, 'sigma': 10, 'category': TradeGoodsCategory.FORESTRY},
    TradeGoods.PITCH: {'inputs': [TradeGoods.WOOD], 'mu': 80, 'sigma': 15, 'category': TradeGoodsCategory.FORESTRY},

    TradeGoods.GRAIN: {'inputs': [None], 'mu': 10, 'sigma': 2, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.HONEY: {'inputs': [None], 'mu': 50, 'sigma': 15, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.HEMP: {'inputs': [None], 'mu': 80, 'sigma': 15, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.FLAX: {'inputs': [None], 'mu': 50, 'sigma': 20, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.SPICES: {'inputs': [None], 'mu': 200, 'sigma': 65, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.DYES: {'inputs': [None], 'mu': 120, 'sigma': 15, 'category': TradeGoodsCategory.FARMING},

    TradeGoods.WINE: {'inputs': [None], 'mu': 150, 'sigma': 20, 'category': TradeGoodsCategory.ALCOHOL},
    TradeGoods.MEAD: {'inputs': [TradeGoods.HONEY], 'mu': 80, 'sigma': 12, 'category': TradeGoodsCategory.ALCOHOL},
    TradeGoods.BEER: {'inputs': [TradeGoods.GRAIN], 'mu': 60, 'sigma': 19, 'category': TradeGoodsCategory.ALCOHOL},
    TradeGoods.FISH: {'inputs': [TradeGoods.SALT], 'mu': 60, 'sigma': 9, 'category': TradeGoodsCategory.FISHING},

    TradeGoods.SALT: {'inputs': [None], 'mu': 50, 'sigma': 8, 'category': TradeGoodsCategory.FISHING},
    TradeGoods.OIL: {'inputs': [TradeGoods.FISH], 'mu': 100, 'sigma': 20, 'category': TradeGoodsCategory.FISHING},

    TradeGoods.MEAT: {'inputs': [TradeGoods.SALT], 'mu': 120, 'sigma': 25, 'category': TradeGoodsCategory.RANCHING},
    TradeGoods.CHEESE: {'inputs': [TradeGoods.SALT], 'mu': 200, 'sigma': 60, 'category': TradeGoodsCategory.RANCHING},
    TradeGoods.PELTS: {'inputs': [None], 'mu': 150, 'sigma': 18, 'category': TradeGoodsCategory.RANCHING},
    TradeGoods.WOOL: {'inputs': [None], 'mu': 90, 'sigma': 15, 'category': TradeGoodsCategory.RANCHING},

    TradeGoods.IRON: {'inputs': [None], 'mu': 150, 'sigma': 47, 'category': TradeGoodsCategory.MINING},
    TradeGoods.GEMS: {'inputs': [None], 'mu': 400, 'sigma': 68, 'category': TradeGoodsCategory.MINING},

    TradeGoods.TOOLS: {'inputs': [TradeGoods.WOOD, TradeGoods.IRON, ], 'mu': 540, 'sigma': 120, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.WEAPONS: {'inputs': [TradeGoods.WOOD, TradeGoods.IRON, TradeGoods.TOOLS], 'mu': 700, 'sigma': 150, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.ARMOR: {'inputs': [TradeGoods.WOOD, TradeGoods.IRON, TradeGoods.TOOLS, TradeGoods.CLOTHING], 'mu': 650, 'sigma': 120, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.JEWELRY: {'inputs': [TradeGoods.IRON, TradeGoods.GEMS, TradeGoods.TOOLS], 'mu': 1000, 'sigma': 200, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.FURNITURE: {'inputs': [TradeGoods.WOOD, TradeGoods.LINEN, TradeGoods.PELTS, TradeGoods.IRON],
                           'mu': 300, 'sigma': 40, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS}
}
CITIES = {
    'antwerp': {
        'region': Region.ENGLISH_CHANNEL,
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
            TradeGoodsCategory.TEXTILES: [TradeGoods.LINEN, TradeGoods.CLOTHING],
            TradeGoodsCategory.FARMING: [TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY],
            TradeGoodsCategory.RANCHING: [
                TradeGoods.WOOL, TradeGoods.PELTS, TradeGoods.CHEESE]
        }},
    'bruges': {
        'region': Region.ENGLISH_CHANNEL,
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
            TradeGoodsCategory.TEXTILES: [TradeGoods.LINEN, TradeGoods.BROADCLOTH, TradeGoods.CLOTHING],
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.SPICES, TradeGoods.HONEY],
            TradeGoodsCategory.RANCHING: [
                TradeGoods.WOOL, TradeGoods.PELTS, TradeGoods.CHEESE]
        }},
    'bergen': {
        'region': Region.NORTH_SEA,
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
            TradeGoodsCategory.FISHING: [TradeGoods.FISH, TradeGoods.OIL],
            TradeGoodsCategory.FORESTRY: [
                TradeGoods.WOOD, TradeGoods.CHARCOAL, TradeGoods.PITCH]
        }},
    'bremen': {
        'region': Region.NORTH_SEA,
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
            TradeGoodsCategory.ALCOHOL: [TradeGoods.MEAD, TradeGoods.BEER, TradeGoods.WINE],
            TradeGoodsCategory.RANCHING: [TradeGoods.PELTS, TradeGoods.WOOL, TradeGoods.CHEESE],
            TradeGoodsCategory.FARMING: [
                TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY]
        }},
    'cologne': {
        'region': Region.ENGLISH_CHANNEL,
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
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.TOOLS, TradeGoods.WEAPONS, TradeGoods.ARMOR, TradeGoods.JEWELRY, TradeGoods.FURNITURE],
            TradeGoodsCategory.RANCHING: [TradeGoods.MEAT, TradeGoods.CHEESE, TradeGoods.PELTS, TradeGoods.WOOL],
            TradeGoodsCategory.MINING: [TradeGoods.IRON, TradeGoods.GEMS],
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY, TradeGoods.SPICES],
            TradeGoodsCategory.ALCOHOL: [TradeGoods.WINE, TradeGoods.BEER, TradeGoods.MEAD]}},
    'danzig': {
        'region': Region.SOUTH_BALTIC,
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
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.HONEY],
            TradeGoodsCategory.MINING: [TradeGoods.IRON, TradeGoods.GEMS], }
    },
    'hamburg': {
        'region': Region.NORTH_SEA,
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
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.JEWELRY, TradeGoods.FURNITURE],
            TradeGoodsCategory.FISHING: [
                TradeGoods.SALT, TradeGoods.FISH, TradeGoods.OIL]
        }
    },
    'kampen': {
        'region': Region.NORTH_SEA,
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
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.JEWELRY, TradeGoods.FURNITURE],
            TradeGoodsCategory.FISHING: [TradeGoods.FISH, TradeGoods.OIL, TradeGoods.SALT]}
    },
    'london': {
        'region': Region.ENGLISH_CHANNEL,
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
            TradeGoodsCategory.TEXTILES: [TradeGoods.LINEN, TradeGoods.BROADCLOTH, TradeGoods.CLOTHING],
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.TOOLS, TradeGoods.WEAPONS, TradeGoods.ARMOR, TradeGoods.JEWELRY, TradeGoods.FURNITURE],
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY]},
    },
    'lubeck': {
        'region': Region.SOUTH_BALTIC,
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
            TradeGoodsCategory.FISHING: [TradeGoods.SALT, TradeGoods.FISH, TradeGoods.OIL],
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY],
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.TOOLS, TradeGoods.WEAPONS, TradeGoods.ARMOR, TradeGoods.JEWELRY, TradeGoods.FURNITURE]}
    },
    'malmo': {
        'region': Region.SOUTH_BALTIC,
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
            TradeGoodsCategory.FORESTRY: [TradeGoods.WOOD, TradeGoods.CHARCOAL, TradeGoods.PITCH],
            TradeGoodsCategory.FISHING: [TradeGoods.FISH, TradeGoods.OIL, TradeGoods.SALT],
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.TOOLS, TradeGoods.WEAPONS, TradeGoods.ARMOR]}
    },
    'novorod': {
        'region': Region.NORTH_BALTIC,
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
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY],
            TradeGoodsCategory.RANCHING: [TradeGoods.MEAT, TradeGoods.CHEESE, TradeGoods.PELTS, TradeGoods.WOOL],
            TradeGoodsCategory.MINING: [TradeGoods.IRON, TradeGoods.GEMS]}
    },
    'riga': {
        'region': Region.NORTH_BALTIC,
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
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY],
            TradeGoodsCategory.MINING: [TradeGoods.IRON, TradeGoods.GEMS],
            TradeGoodsCategory.FORESTRY: [TradeGoods.WOOD, TradeGoods.CHARCOAL, TradeGoods.PITCH]},
    },
    'rostock': {
        'region': Region.SOUTH_BALTIC,
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
        'productions': {TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY],
                        TradeGoodsCategory.RANCHING: [TradeGoods.MEAT, TradeGoods.CHEESE, TradeGoods.PELTS, TradeGoods.WOOL],
                        TradeGoodsCategory.FISHING: [TradeGoods.FISH, TradeGoods.SALT]}
    },
    'stockholm': {
        'region': Region.NORTH_BALTIC,
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
            TradeGoodsCategory.MINING: [TradeGoods.IRON, TradeGoods.GEMS],
            TradeGoodsCategory.FORESTRY: [TradeGoods.WOOD, TradeGoods.CHARCOAL, TradeGoods.PITCH]},
    },
    'stralsund': {
        'region': Region.SOUTH_BALTIC,
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
            TradeGoodsCategory.TEXTILES: [TradeGoods.LINEN, TradeGoods.BROADCLOTH, TradeGoods.CLOTHING],
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.SPICES, TradeGoods.HONEY],
            TradeGoodsCategory.RANCHING: [TradeGoods.WOOL, TradeGoods.PELTS, TradeGoods.CHEESE]}
    },
    'tallinn': {
        'region': Region.NORTH_BALTIC,
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
            TradeGoodsCategory.FISHING: [TradeGoods.FISH, TradeGoods.OIL],
            TradeGoodsCategory.FORESTRY: [TradeGoods.WOOD, TradeGoods.CHARCOAL, TradeGoods.PITCH]}
    },
    'visby': {
        'region': Region.NORTH_BALTIC,
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
            TradeGoodsCategory.MANUFACTURED_ITEMS: [TradeGoods.TOOLS, TradeGoods.WEAPONS, TradeGoods.ARMOR, TradeGoods.JEWELRY, TradeGoods.FURNITURE],
            TradeGoodsCategory.RANCHING: [TradeGoods.MEAT, TradeGoods.CHEESE, TradeGoods.PELTS, TradeGoods.WOOL],
            TradeGoodsCategory.MINING: [TradeGoods.IRON, TradeGoods.GEMS],
            TradeGoodsCategory.FARMING: [TradeGoods.GRAIN, TradeGoods.HEMP, TradeGoods.FLAX, TradeGoods.DYES, TradeGoods.HONEY, TradeGoods.SPICES],
            TradeGoodsCategory.ALCOHOL: [TradeGoods.WINE, TradeGoods.BEER, TradeGoods.MEAD]}}
}
TRADING_HOUSE_DIALOGUE = [
    'Ah my lord, come in and welcome! What brings you to the trading house today?', 'Another day another denari!', 'Setting sail? Let me know what I can get loaded for you!']
