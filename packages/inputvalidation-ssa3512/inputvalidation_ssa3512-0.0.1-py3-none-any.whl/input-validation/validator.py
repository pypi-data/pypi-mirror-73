"""
validator.py
Steve Ashman
Basic validation library for console apps
"""


def get_valid_selection(valid_options, display_options):
    """
    Gets a valid selection from stdin matching one of the provided options
    :param valid_options: list of valid options for selection
    :param display_options: function for displaying options to the user
    :return: valid selection from the provided list
    """
    valid = False
    while not valid:
        display_options()
        in_value = input()
        try:
            in_value = int(in_value)
        except ValueError:
            pass
        if in_value in valid_options:
            valid = True
        else:
            print("Invalid input")

    return in_value


def write_invalid_input():
    """
    Prints "Invalid input"
    :return: No return value
    """
    print("Invalid input")


def get_selected_action(in_value, switcher):
    """
    Gets the action for a selected menu item
    :param in_value: validated input value
    :param switcher: dictionary of actions to get value from
    :return: selected action from switcher
    """
    try:
        return switcher.get(in_value, write_invalid_input)
    except ValueError:
        return None
