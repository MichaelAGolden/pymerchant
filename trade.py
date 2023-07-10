from __future__ import annotations
import validators as v


def set_inventory(seller, buyer, item_name, item_qty):
    """
    set_inventory updates buyer and seller inventories at same in transaction

    Args:
        seller (Entity): Entity that is the seller in the context of the transaction
        buyer (Entity): Entity that is the buyer in the context of the transaction
        item_name (str): Name of item that is being traded
        item_qty (int): Quantity of item that is being traded
    """
    # updates seller item quantity
    prior_seller_item_qty = getattr(seller, item_name)
    updated_seller_item_qty = prior_seller_item_qty - item_qty
    setattr(seller, item_name, updated_seller_item_qty)

    # updates buyer item quantity
    prior_buyer_item_qty = getattr(buyer, item_name)
    updated_buyer_item_qty = prior_buyer_item_qty + item_qty
    setattr(buyer, item_name, updated_buyer_item_qty)


def set_gold(seller, buyer, total_trade):
    """
    set_gold updates buyer and seller gold attributes at same time in transaction

    Args:
        seller (Entity): Entity that is the seller in the context of the transaction
        buyer (Entity): Entity that is the buyer in the context of the transaction
        total_trade (int): Total trade value, represented as an integer value
    """
    # updates seller gold
    prior_seller_gold = getattr(seller, 'gold')
    updated_seller_gold = prior_seller_gold + total_trade
    setattr(seller, 'gold', updated_seller_gold)

    # updates buyer gold
    prior_buyer_gold = getattr(buyer, 'gold')
    updated_buyer_gold = prior_buyer_gold - total_trade
    setattr(buyer, 'gold', updated_buyer_gold)


def log_transaction(player, market, item_name, item_price, item_qty):
    pass


def trade(player, market, trade_type, item_name, item_price, item_qty):
    total_trade = item_price * item_qty
    if trade_type == 'buy':
        v.Validators.affordability_check(total_trade, player, trade)
        v.Validators.check_inventory_capacity(item_qty, player, trade)
        set_gold(player, market, total_trade)
        set_inventory(player, market, item_name, item_qty)
        log_transaction(player, market, item_name,
                        item_qty, item_price, total_trade)
    elif trade_type == 'sell':
        set_gold(market, player)
        set_inventory(market, player)
        log_transaction(market, player, item_name,
                        item_qty, item_price)


class Transaction:
    """
     _summary_
     Transaction class provides class method provides a way to dynamically store transactions between player and markets as its own datatype, encapsulating all information necessary to understand the transaction and is the base input for all logging
    """
    pass
