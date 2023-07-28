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
        "The latest fashion trend in Bruges has caused an increase in demand for textiles such as ."
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
    ]}
MARKET_GOODS = {
    TradeGoods.LINEN: {'inputs': [TradeGoods.HEMP, TradeGoods.FLAX], 'base_price': 10, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.TEXTILES},
    TradeGoods.BROADCLOTH: {'inputs': [TradeGoods.WOOL, TradeGoods.DYES], 'base_price': 100, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.TEXTILES},
    TradeGoods.CLOTHING: {'inputs': [TradeGoods.LINEN, TradeGoods.WOOL, TradeGoods.PELTS, TradeGoods.DYES], 'base_price': 120, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.TEXTILES},

    TradeGoods.WOOD: {'inputs': [None], 'base_price': 30, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FORESTRY},
    TradeGoods.CHARCOAL: {'inputs': [TradeGoods.WOOD], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FORESTRY},
    TradeGoods.PITCH: {'inputs': [TradeGoods.WOOD], 'base_price': 80, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FORESTRY},

    TradeGoods.GRAIN: {'inputs': [None], 'base_price': 30, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.HONEY: {'inputs': [None], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.HEMP: {'inputs': [None], 'base_price': 80, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.FLAX: {'inputs': [None], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.SPICES: {'inputs': [None], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FARMING},
    TradeGoods.DYES: {'inputs': [None], 'base_price': 120, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FARMING},

    TradeGoods.WINE: {'inputs': [None], 'base_price': 150, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.ALCOHOL},
    TradeGoods.MEAD: {'inputs': [TradeGoods.HONEY], 'base_price': 80, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.ALCOHOL},
    TradeGoods.BEER: {'inputs': [TradeGoods.GRAIN], 'base_price': 60, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.ALCOHOL},
    TradeGoods.FISH: {'inputs': [TradeGoods.SALT], 'base_price': 60, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FISHING},

    TradeGoods.SALT: {'inputs': [None], 'base_price': 50, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FISHING},
    TradeGoods.OIL: {'inputs': [TradeGoods.FISH], 'base_price': 100, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.FISHING},

    TradeGoods.MEAT: {'inputs': [TradeGoods.SALT], 'base_price': 120, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.RANCHING},
    TradeGoods.CHEESE: {'inputs': [TradeGoods.SALT], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.RANCHING},
    TradeGoods.PELTS: {'inputs': [None], 'base_price': 150, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.RANCHING},
    TradeGoods.WOOL: {'inputs': [None], 'base_price': 90, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.RANCHING},

    TradeGoods.IRON: {'inputs': [None], 'base_price': 100, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MINING},
    TradeGoods.GEMS: {'inputs': [None], 'base_price': 400, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MINING},

    TradeGoods.TOOLS: {'inputs': [TradeGoods.WOOD, TradeGoods.IRON, ], 'base_price': 150, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.WEAPONS: {'inputs': [TradeGoods.WOOD, TradeGoods.IRON, TradeGoods.TOOLS], 'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.ARMOR: {'inputs': [TradeGoods.WOOD, TradeGoods.IRON, TradeGoods.TOOLS, TradeGoods.CLOTHING], 'base_price': 300, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.JEWELRY: {'inputs': [TradeGoods.IRON, TradeGoods.GEMS, TradeGoods.TOOLS], 'base_price': 1000, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS},
    TradeGoods.FURNITURE: {'inputs': [TradeGoods.WOOD, TradeGoods.LINEN, TradeGoods.PELTS, TradeGoods.IRON],
                           'base_price': 200, 'demand_sigma': 0.5, 'supply_sigma': 0.5, 'category': TradeGoodsCategory.MANUFACTURED_ITEMS}
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
