# author: Elior Papiernik (elior.papiernik@gmail.com)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import pprint

emoji_back = "<-"


def get_menu(path: list):
    menu = menus
    for elem in path:
        menu = menu[int(elem)][1]
    return menu


def load_data():
    final_array = []
    with open("./data.json") as file:
        jsondata = json.load(file)
        build_array(final_array, jsondata)
    return final_array


def build_array(array, data):
    for elem in data:
        if type(data[elem]) is str:
            array.append((elem, data[elem]))
        else:
            array_bext = []
            build_array(array_bext, data[elem])
            array.append((elem, array_bext))


# Each menu is a list of tuples
menus = load_data()


def build_keyboard_with_origin(path: str, width=1):
    pathlist = path.split(" ")
    menu = get_menu(pathlist)

    keyboard = []
    col = []

    # Add the list of buttons
    for i in range(0, menu.__len__()):
        col.append(InlineKeyboardButton(
            menu[i][0], callback_data=path + " " + str(i)))
        if i >= width:
            keyboard.append(col)
            col = []

    # Add the back button
    if len(pathlist) > 0:
        col.append(
            InlineKeyboardButton(emoji_back, callback_data=path))
    keyboard.append(col)

    return InlineKeyboardMarkup(keyboard)
