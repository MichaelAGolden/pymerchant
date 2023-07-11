from trade import *


def main():
    linen = Item(name='linen', quantity=0,
                 category=Category.TEXTILES, inputs=[None])
    wool = Item(name='wool', quantity=0, category=Category.TEXTILES,
                inputs=[None])
    print(linen)
    linen.update_quantity(10)
    market_inv = Inventory(linen=linen, wool=wool, gold=100)
    print(market_inv)


if __name__ == '__main__':
    main()
