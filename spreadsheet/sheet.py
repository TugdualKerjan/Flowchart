# author: Elior Papiernik (elior.papiernik@gmail.com)

import gspread
from pathlib import Path

path = Path(__file__).parent / "service_account.json"
gc = gspread.service_account(filename=path)

SPREADSHEET_NAME = "Bot text"

spreadsheet = gc.open(SPREADSHEET_NAME)
messages_sheet = spreadsheet.worksheet("Phrases")
buttons_sheet = spreadsheet.worksheet("Boutons")
others_sheet = spreadsheet.worksheet("Autres")

messages = {}


def update_messages(d):
    """Updates the dict containing the messages"""

    global messages

    messages = d

    return


def get_dict_phrases():
    values = messages_sheet.get_all_values()
    values.remove(values[0])

    d = {}

    if not values:
        print('No data found.')
    else:
        for row in values:
            d[row[0]] = {
                "fr": row[1],
                "en": row[2]
            }
    return d


def get_dict_buttons():
    values = buttons_sheet.get_all_values()
    values.remove(values[0])

    d = {}

    if not values:
        print('No data found.')
    else:
        for row in values:
            d[row[0]] = {
                "fr": row[1],
                "en": row[2]
            }
    return d


def get_dict_messages():
    values = others_sheet.get_all_values()
    values.remove(values[0])

    d = {}

    if not values:
        print('No data found.')
    else:
        for row in values:
            d[row[0]] = {
                "fr": row[1],
                "en": row[2]
            }
    return d
