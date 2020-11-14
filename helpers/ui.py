# author: Elior Papiernik (elior.papiernik@gmail.com)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
sections = ["AR", "CGC", "CMS", "EL", "GC", "GM",
            "IC", "MA", "MT", "MX", "PH", "SIE", "SV", "MTE"]
years = ["BA1", "BA3", "BA5", "MA1", "MA3"]
datas = [del_all, forget]
message_on_cloud = [use, suggest, create_username]
reg_buttons = [reg_button, unreg_button]
regable_menus = [courses, sports, cooking, video_games, coffee, music]

emoji_back = "⬅️"
emoji_checked = "☑️️️"

special = sections + years + list(languages) + message_on_cloud + reg_buttons + regable_menus + datas + \
    [language, section, year, data, start, share_username,
        share_contact, stats, share_phone_number]

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


def build_keyboard_with_origin(arg_stacktrace: list, width=1):
    stacktrace = arg_stacktrace.copy()
    args = menus[stacktrace[0]]

    keyboard = []
    column = []
    for arg in args:
        column.append(InlineKeyboardButton(
            buttons_menu[arg][l], callback_data=arg + " " + " ".join(stacktrace)))
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
        column.append(InlineKeyboardButton(
            buttons_simple[arg], callback_data=start + " " + arg))
        if len(column) >= width:
            keyboard.append(column)
            column = []
    keyboard.append(column)

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
