# author: Elior Papiernik (elior.papiernik@gmail.com)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

menus = {
    "menu": {
        "a": {
            "menu b": "b",
            "menu c": "c"
        },
        "b": {
            "menu a": "a",
            "menu c": "c"
        },
        "c": {"b": "b", "a": "a"},
    }
}

emoji_back = "<-"

#


def build_keyboard_with_origin(arg_stacktrace: list, width=1):
    stacktrace = arg_stacktrace.copy()
    menu = menus[stacktrace[0]]

    keyboard = []
    col = []

    # Add the list of buttons
    for button in menu.keys():
        col.append(InlineKeyboardButton(
            button, callback_data=button + " " + " ".join(stacktrace)))
        if len(col) >= width:
            keyboard.append(col)
            col = []

    # Add the back button
    stacktrace.pop(0)
    if len(stacktrace) != 0:
        col.append(
            InlineKeyboardButton(emoji_back, callback_data=" ".join(stacktrace)))
    keyboard.append(col)

    return InlineKeyboardMarkup(keyboard)

# # Reply
# def build_keyboard_only_back(arg_stacktrace: list):
#     stacktrace = arg_stacktrace.copy()

#     keyboard = []

#     stacktrace.pop(0)
#     keyboard.append(
#         [InlineKeyboardButton(emoji_back + " " + buttons_menu[stacktrace[0]], callback_data=" ".join(stacktrace))])

#     return InlineKeyboardMarkup(keyboard)

# Display start menu


def build_keyboard_start(width=1):
    keyboard = []
    col = []
    for button in menus.keys():
        col.append(InlineKeyboardButton(
            button, callback_data=button + " menu"))
        if len(col) >= width:
            keyboard.append(col)
            col = []
    keyboard.append(col)

    return InlineKeyboardMarkup(keyboard)

# stats_messages = {
#     fr: "Utilisateurs enregistrés : {}\n{}Pour un total de {} mises en relation",
#     en: "Users registered: {}\n{}For a total of {} pairings"
# }
# stats_domain_message = {
#     fr: " mises en relation pour ",
#     en: " pairings to "
# }


# def stats_message(l) -> str:
#     total_users = sql.get_nb_users()
#     total_domains = 0
#     str_domains = ""
#     for domain in regable_menus:
#         nb_pairings = sql.get_nb_pairings_domain(domain)
#         total_domains += nb_pairings
#         str_domains += "\t\t\t\t" + str(nb_pairings) + stats_domain_message[l] + buttons_menu[domain][l] + "\n"
#     return stats_messages[l].format(total_users, str_domains, total_domains)
