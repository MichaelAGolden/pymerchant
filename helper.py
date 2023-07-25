

GET_NUMBER_INPUT = "Enter the number cooresponding to your choice: "
INVALID_CHOICE_NUMBER_IN_RANGE = "Invalid choice. Please enter a number between 1 and {len_list_to_check}"


def range_of_list(list_to_check):
    valid = False
    while not valid:
        choice = input(GET_NUMBER_INPUT)
        try:
            choice = int(choice)
            valid = True
        except ValueError:
            print(INVALID_CHOICE_NUMBER_IN_RANGE.format(
                len_list_to_check=len(list_to_check)))
    return choice


def buying_or_selling():
    while not valid:
        choice = input("Buying or Selling (enter B/S): ")
        try:
            if choice.upper() == 'B':
                user_selection = 'buying'
                valid = True
            elif choice.upper() == 'S':
                user_selection = 'selling'
                valid = True
            else:
                raise ValueError
        except ValueError:
            print("Invalid entry: Please enter B for Buying or S for Selling")
    return user_selection


def check_inventory_capacity(user_input_qty: int, player):
    try:
        if user_input_qty > player.get_capacity():
            raise ValueError
    except ValueError:
        print("You don't have enough space in your inventory for that.")


def affordability_check(item_cost: int, player):
    try:
        if item_cost > player.gold:
            raise ValueError
    except ValueError:
        print("You don't have enough gold for that.")
