# author: Elior Papiernik (elior.papiernik@gmail.com)

import os, telegram
from telegram import Update, Message
from telegram.ext import CallbackContext

from . import sql, ui

from spreadsheet import sheet

bot = telegram.Bot(os.environ["BOT_TOKEN"])

quit = "quit"


def fetch_message_id(message: Message) -> int:
    """Returns id fetched from a Message"""

    return message.message_id


def fetch_id_telegram(update: Update) -> int:
    """Returns id_telegram fetched from an Update"""

    if update.message:
        return update.message.from_user.id
    elif update.callback_query:
        return update.callback_query.from_user.id
    else:
        return 0


def fetch_first_name(update: Update) -> str:
    """Returns first_name fetched from an Update"""

    if update.message:
        return update.message.from_user.first_name
    elif update.callback_query:
        return update.callback_query.from_user.first_name
    else:
        return ""


def fetch_username(update: Update) -> str:
    """Returns username fetched from an Update"""

    if update.message:
        return update.message.from_user.username
    elif update.callback_query:
        return update.callback_query.from_user.username
    else:
        return ""


def fetch_phone_number(update: Update, l) -> str:
    """Returns phone_number fetched from an Update"""

    if update.message and update.message.reply_to_message and update.message.contact and update.message.reply_to_message.text == ui.message(ui.ask_phone_or_cancel, l):
        return update.message.contact.phone_number
    else:
        return ""


def user_quits(id_telegram, l) -> None:
    """Sends the appropriate message to the user when he unregisters from the system"""

    delete_message(id_telegram, sql.get_menu_id(id_telegram))
    delete_contacts_pairings(id_telegram)
    bot.send_message(id_telegram, sheet.messages[quit][l])

    return


def send_contact(l, domain, id_target, id_contact):
    """Sends to user target the contact of user contact"""

    contact_first_name = sql.get_one_from_users_with_id_telegram(sql.first_name, id_contact)

    contact_username = sql.get_username(id_contact)

    if ui.courses in domain:
        domain = ui.courses

    if contact_username is not None:
        message = bot.send_message(id_target, ui.message(ui.send_contact_username, l).format(ui.buttons_menu[domain][l], contact_first_name, contact_username))
        sql.add_pairing(id_target, id_contact, message.message_id, True)
    else:
        contact_phone_number = sql.get_one_from_users_with_id_telegram(sql.phone_number, id_contact)
        message = bot.send_message(id_target, ui.message(ui.send_contact_phone, l).format(ui.buttons_menu[domain][l], contact_first_name))
        bot.send_contact(id_target, first_name=contact_first_name, phone_number=contact_phone_number)
        sql.add_pairing(id_target, id_contact, message.message_id, False)

    return


def delete_message(id_telegram, id_message):
    """Deletes the message with given id in given chat"""

    bot.delete_message(id_telegram, id_message)

    return


def send_main_message(id_telegram):
    """Sends the main menu to the given chat"""

    l = sql.get_language(id_telegram)
    text = ui.message(ui.main, l)
    keyboard = ui.build_keyboard_with_origin(l, [ui.main])

    message = bot.send_message(id_telegram, text, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)

    sql.set_menu_id(id_telegram, fetch_message_id(message))

    return


def delete_contacts_pairings(telegram_id):
    pairings = sql.get_all_pairings_of_user(telegram_id)

    print(pairings)

    for pairing in pairings:
        delete_message(pairing[2], pairing[4])
        if pairings[5] is False:
            delete_message(pairing[2], pairing["""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""])

    return
