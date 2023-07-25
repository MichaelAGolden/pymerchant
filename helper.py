
def range_of_list(list_to_check):
    valid_input = False
    while not valid_input:
        choice = input("Enter the number corresponding to your choice: ")
        try:
            choice = int(choice)
            valid_input = True
        except ValueError:
            print(
                f"Invalid choice. Please enter a number between 1 and {len(list_to_check)}.")
    return choice


def check_inventory_capacity(self, user_input_qty: int, player: Type[Player], return_function: Callable):
    """
    Check_inventory_capacity Checks that the player has enough space in their inventory for the quantity of items they are trying to add.

    Args:
        user_input_qty (int): _description_
        player (Player): _description_
        return_function (Callable): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    try:
        if user_input_qty > player.get_capacity():
            raise ValueError
    except ValueError:
        print(lack_of_space :=
              "You don't have enough space in your inventory for that.")
        return return_function(lack_of_space)


@classmethod
def affordability_check(self, item_cost: int, player: Type[Player], return_function: Callable):
    """
    Affordability_check Checks that the player has enough gold to afford the item they are trying to buy.

    Args:
        item_cost (int): _description_
        player (Player): _description_
        return_function (Callable): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    try:
        if item_cost > player.gold:
            raise ValueError
    except ValueError:
        print(not_enough_gold := "You don't have enough gold for that.")
        return return_function(not_enough_gold)
