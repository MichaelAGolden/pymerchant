from __future__ import annotations
import random
import market as mk
from player import Player
import game
random.seed(123)


lubek = mk.Market("Lubek", 1, [])
hamburg = mk.Market("Hamburg", 3, [])
bremen = mk.Market("Bremen", 2, [])
berlin = mk.Market("Berlin", 4, [])
rostock = mk.Market("Rostock", 2, [])


lubek.connected_cities = [hamburg, bremen, berlin, rostock]
hamburg.connected_cities = [lubek, bremen, berlin]
bremen.connected_cities = [hamburg, berlin]
berlin.connected_cities = [lubek, berlin]
rostock.connected_cities = [lubek, berlin]


merchant = Player("merchant", 1000, lubek)


# move game loop to seperate file
app = game.Game(merchant)
# print("MARKET INVENTORY")
# print(lubek.market_inventory)
# print("\n\n\nMarket_Inventory.items()")
# print(lubek.market_inventory.items())
# print("\n\n\nMarket_Inventory.values()")
# print(lubek.market_inventory.values())
# print("\n\n\nMarket_Inventory.keys()")
# print(lubek.market_inventory.keys())
# print("\n\n\nGET_MARKET_LISTINGS()")
# print(lubek.get_market_listings())
app.game_loop()
