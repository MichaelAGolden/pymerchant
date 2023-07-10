from __future__ import annotations
import validators as v


class Transaction:

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def log_transaction(self, player, market, item_name, item_price, item_qty):
        pass

    def set_gold(self, seller, buyer, total_trade):
        # sets buyer and seller new gold values in same function to ensure completion
        prior_seller_gold = getattr(seller, 'gold')
        updated_seller_gold = prior_seller_gold + total_trade
        setattr(seller, 'gold', updated_seller_gold)

        prior_buyer_gold = getattr(buyer, 'gold')
        updated_buyer_gold = prior_buyer_gold - total_trade
        setattr(buyer, 'gold', updated_buyer_gold)


def trade(self, player, market, trade_type, item_name, item_price, item_qty):
    total_trade = item_price * item_qty
    if trade_type == 'buy':
        v.Validators.affordability_check(total_trade, player, self.trade)
        v.Validators.check_inventory_capacity(item_qty, player, self.trade)
        self.set_gold(player, market, total_trade)
        self.set_inventory(player, market, item_name, item_qty)
        self.log_transaction(player, market, item_name,
                             item_qty, item_price, total_trade)
    elif trade_type == 'sell':
        self.set_gold(market, player)
        self.set_inventory(market, player)
        self.log_transaction(market, player, item_name, item_qty, item_price)
