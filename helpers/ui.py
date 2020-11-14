# author: Elior Papiernik (elior.papiernik@gmail.com)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from . import sql

en = "en"
fr = "fr"

default_language = en

messages = {}
buttons_menu = {}
buttons_simple = {}

start = "start"
main = "main"
about = "about"
search = "search"
data = "data"
sports = "sports"
courses = "courses"
cooking = "cooking"
video_games = "video_games"
coffee = "coffee"
music = "music"
params = "params"
section = "section"
year = "year"
language = "language"
use = "use"
suggest = "suggest"
stats = "stats"
del_all = "del_all"
forget = "forget"
share_contact = "share_contact"
share_username = "share_username"
create_username = "create_username"
share_phone_number = "share_phone_number"
send_contact_phone = "send_contact_phone"
send_contact_username = "send_contact_username"
ask_phone_or_cancel = "ask_phone_or_cancel"

reg_button = "reg_button"
unreg_button = "unreg_button"

random = "random"

languages = {"fr": "🇫🇷 Français", "en": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 English"}
sections = ["AR", "CGC", "CMS", "EL", "GC", "GM", "IC", "MA", "MT", "MX", "PH", "SIE", "SV", "MTE"]
years = ["BA1", "BA3", "BA5", "MA1", "MA3"]
datas = [del_all, forget]
message_on_cloud = [use, suggest, create_username]
reg_buttons = [reg_button, unreg_button]
regable_menus = [courses, sports, cooking, video_games, coffee, music]

emoji_back = "⬅️"
emoji_checked = "☑️️️"

special = sections + years + list(languages) + message_on_cloud + reg_buttons + regable_menus + datas + \
          [language, section, year, data, start, share_username, share_contact, stats, share_phone_number]

menus = {
    start: languages,
    share_contact: [share_username, create_username, share_phone_number],
    main: [search, params, about],
    search: [coffee, cooking, sports, courses, music, video_games],
    about: [use, suggest, stats],
    params: [language, section, year, data],
    data: datas,
    section: sections,
    year: years,
    language: languages
}

for reg in regable_menus:
    menus[reg] = reg_buttons

menus_layout = {
    main: 1,
    search: 2,
    params: 3,
    about: 3,
    share_contact: 1,
    language: 2,
    section: 2,
    year: 2
}

languages_layout = 2
sections_layout = 3
years_layout = 3


# === SETUP ===

def setup_buttons():
    for l in languages:
        buttons_simple[l] = languages[l]
    for s in sections:
        buttons_simple[s] = s
    for y in years:
        buttons_simple[y] = y

    return


def update_messages(d):
    """Updates the dict containing the messages"""

    global messages

    messages = d

    return


def update_buttons(d):
    """Updates the dict containing the buttons"""

    global buttons_menu

    buttons_menu = d
    setup_buttons()

    return


def build_keyboard_with_origin(l, arg_stacktrace: list, width=1):
    stacktrace = arg_stacktrace.copy()
    args = menus[stacktrace[0]]

    keyboard = []
    column = []
    for arg in args:
        column.append(InlineKeyboardButton(buttons_menu[arg][l], callback_data=arg + " " + " ".join(stacktrace)))
        if len(column) >= width:
            keyboard.append(column)
            column = []

    stacktrace.pop(0)
    if len(stacktrace) != 0:
        column.append(
            InlineKeyboardButton(emoji_back + " " + buttons_menu[stacktrace[0]][l], callback_data=" ".join(stacktrace)))
    keyboard.append(column)

    return InlineKeyboardMarkup(keyboard)


def build_keyboard_only_back(l, arg_stacktrace: list):
    stacktrace = arg_stacktrace.copy()

    keyboard = []

    stacktrace.pop(0)
    keyboard.append(
        [InlineKeyboardButton(emoji_back + " " + buttons_menu[stacktrace[0]][l], callback_data=" ".join(stacktrace))])

    return InlineKeyboardMarkup(keyboard)


def build_keyboard_start(l, width=1):
    keyboard = []
    column = []
    for arg in menus[start]:
        column.append(InlineKeyboardButton(buttons_simple[arg], callback_data=start + " " + arg))
        if len(column) >= width:
            keyboard.append(column)
            column = []
    keyboard.append(column)

    return InlineKeyboardMarkup(keyboard)


def build_keyboard_share_contact(l, width=1):
    """Careful with this method, build up has been created to be consistent with the use of _only_back method"""
    # TODO change to be independent of only back implementation

    keyboard = []

    column = [InlineKeyboardButton(buttons_menu[share_username][l], callback_data=share_username)]
    keyboard.append(column)

    column = [InlineKeyboardButton(buttons_menu[create_username][l], callback_data=create_username + " " + share_contact)]
    keyboard.append(column)

    column = [InlineKeyboardButton(buttons_menu[share_phone_number][l], callback_data=share_phone_number)]
    keyboard.append(column)

    return InlineKeyboardMarkup(keyboard)


def build_keyboard_check_param(l, arg_stacktrace: list, args, arg_data="", width=1):
    stacktrace = arg_stacktrace.copy()

    keyboard = []
    column = []
    for arg in args:
        column.append(
            InlineKeyboardButton(get_buttons_check_value(arg, l) + (" " + emoji_checked if arg == arg_data else ""),
                                 callback_data=arg + " " + " ".join(stacktrace)))
        if len(column) >= width:
            keyboard.append(column)
            column = []

    stacktrace.pop(0)
    if len(stacktrace) != 0:
        column.append(
            InlineKeyboardButton(emoji_back + " " + buttons_menu[stacktrace[0]][l], callback_data=" ".join(stacktrace)))
    keyboard.append(column)

    return InlineKeyboardMarkup(keyboard)


def get_buttons_check_value(arg, l):
    if arg in buttons_simple:
        return buttons_simple[arg]
    elif arg in buttons_menu:
        return buttons_menu[arg][l]

    return None


def build_keyboard_registration(l, arg_stacktrace: list, registered: bool, width=1):
    stacktrace = arg_stacktrace.copy()

    keyboard = []
    button = unreg_button if registered else reg_button
    column = [InlineKeyboardButton(buttons_menu[button][l],
                                   callback_data=button + " " + " ".join(stacktrace))]
    if len(column) >= width:
        keyboard.append(column)
        column = []

    stacktrace.pop(0)
    if len(stacktrace) != 0:
        column.append(
            InlineKeyboardButton(emoji_back + " " + buttons_menu[stacktrace[0]][l], callback_data=" ".join(stacktrace)))
    keyboard.append(column)

    return InlineKeyboardMarkup(keyboard)


def message(name, l) -> str:
    return messages[name][l]


stats_messages = {
    fr: "Utilisateurs enregistrés : {}\n{}Pour un total de {} mises en relation",
    en: "Users registered: {}\n{}For a total of {} pairings"
}
stats_domain_message = {
    fr: " mises en relation pour ",
    en: " pairings to "
}


def stats_message(l) -> str:
    total_users = sql.get_nb_users()
    total_domains = 0
    str_domains = ""
    for domain in regable_menus:
        nb_pairings = sql.get_nb_pairings_domain(domain)
        total_domains += nb_pairings
        str_domains += "\t\t\t\t" + str(nb_pairings) + stats_domain_message[l] + buttons_menu[domain][l] + "\n"
    return stats_messages[l].format(total_users, str_domains, total_domains)
