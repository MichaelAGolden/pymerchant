import market
from trade import Item, Inventory


class Player:
    location: market.Market

    def __init__(self, name, gold, location) -> None:
        self.name = name
        self.gold = gold
        self.location = location
        self.max_capacity: float = 300
        self.inventory = Inventory(gold=1000)

    def __repr__(self):
        return str(f"[{self.name}, {self.gold}, {self.inventory}, {self.location.name}]")

    def init_inventory(self):
        items = self.location.BASE_PRICES
        return {item: {'quantity': 0, 'last_purchase_price': 0, 'avg_cost': 0} for item in items}

    def get_capacity(self):
        self.max_capacity
        self.load = sum([self.inventory[item]['quantity']
                        for item in self.inventory])
        return self.max_capacity - self.load

    def buy_update_inventory(self, item_name, quantity, price, item_cost):

        self.gold = self.gold - item_cost
        self.inventory[item_name]['quantity'] += quantity
        self.inventory[item_name]['avg_cost'] = (
            self.inventory[item_name]['avg_cost'] + item_cost) / ((self.inventory[item_name]['quantity']) + quantity)
        self.inventory[item_name]['last_purchase_price'] = price

    def show_inventory(self):
        table_heading = "-----------------Player Inventory--------------------"
        table_labels = "---Good---|---Qty---|--avgCost--|---Purchase Price---"
        short_inventory = [f"--{item_name}--|----{info['quantity']}----|----info['avg_cost']----|----info['last_purchase_price']----"
                           for item_name, info in self.inventory.goods.items() if item_name.quantity > 0]

        return table_heading + '\n' + table_labels + '\n' + '\n'.join(short_inventory)


def main():
    lubeck = market.Market('lubeck', 2)
    me = Player('michael', 1000, lubeck)
    # print(me)
    # print(me.inventory)
    print(me.inventory.goods.keys())
    # print(me.show_inventory())


if __name__ == '__main__':
    main()
