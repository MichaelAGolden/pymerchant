from __future__ import annotations
from typing import Type, Callable


class Validators:
    def __init__(self) -> None:
        pass

    def range_of_list(user_input: int, list_to_check: list, return_function: Callable):
        """range_of_list Provides validation for user input when checking that input is within a range from 1 to the length of a list of ints.

        Args:
            user_input (int): int value from user input
            list_to_check (list): list to check length of and compare to user_input

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        try:
            if user_input < 1 or user_input > len(list_to_check):
                raise ValueError
        except ValueError:
            print(
                invalid_input := f"Invalid choice. Please enter a number between 1 and {len(list_to_check)}.")
            return return_function(invalid_input)

    def check_inventory_capacity(user_input_qty: int, player: Type[Player], return_function: Callable):
        """check_inventory_capacity Checks that the player has enough space in their inventory for the quantity of items they are trying to add.

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

    def affordability_check(item_cost: int, player: Type[Player], return_function: Callable):
        """affordability_check Checks that the player has enough gold to afford the item they are trying to buy.

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
