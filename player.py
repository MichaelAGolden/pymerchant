

class Player:

    def __init__(self, name, gold, location) -> None:
        self.name = name
        self.gold = gold
        self.location = location
        self.max_capacity: float = 300
        self.inventory = self.init_inventory()

    def __repr__(self):
        return str(f"[{self.name}, {self.gold}, {self.inventory}, {self.location.name}]")

    def init_inventory(self):
        items = self.location.ITEM_LIST
        return {k: {'quantity': 0, 'avg_cost': 0.0, 'last_purchase_price': 0.0, 'weight_multiple': v['weight_multiple']} for k, v in items.items()}

    def get_capacity(self):
        self.max_capacity
        self.load = sum([v['quantity'] * v['weight_multiple']
                        for v in self.inventory.values()])
        return self.max_capacity - self.load

    def update_inventory(self, item_name, quantity, price, item_cost):
        self.gold = self.gold - item_cost
        self.inventory[item_name]['quantity'] += quantity
        self.inventory[item_name]['avg_cost'] = (
            self.inventory[item_name]['avg_cost'] + item_cost) / ((self.inventory[item_name]['quantity']) + quantity)
        self.inventory[item_name]['last_purchase_price'] = price
        self.inventory[item_name]['weight_multiple'] = self.location.ITEM_LIST[item_name]['weight_multiple']

    def show_inventory(self):
        short_inventory = [f"{k}: {v['quantity']}"
                           for k, v in self.inventory.items()]
        return '\n' + '\n'.join(short_inventory)
