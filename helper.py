
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
