# author: Elior Papiernik (elior.papiernik@gmail.com)

import os

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler

from helpers import sql
from helpers import mytelegram
from helpers import ui
from helpers import menus

from spreadsheet import sheet


def setup():
    ui.update_messages(sheet.get_dict_phrases())
    ui.update_buttons(sheet.get_dict_buttons())
    sheet.update_messages(sheet.get_dict_messages())


def bot_start(update: Update, context: CallbackContext) -> None:
    """Bot start command"""

    # register user if not already in database
    id_telegram = mytelegram.fetch_id_telegram(update)
    if not sql.exist_user(id_telegram):
        sql.register_user(id_telegram, mytelegram.fetch_first_name(update))

    # remove /start message from user
    try:
        context.bot.delete_message(update.message.chat.id, update.message.message_id)
        if update.message.message_id > 1:
            context.bot.delete_message(update.message.chat.id, update.message.message_id - 1)
    except:
        pass

    l = sql.get_language(mytelegram.fetch_id_telegram(update))
    message = update.message.reply_text(ui.message(ui.start, l),
                                        reply_markup=ui.build_keyboard_start(l, ui.languages_layout),
                                        parse_mode=telegram.ParseMode.MARKDOWN)

    sql.set_menu_id(id_telegram, mytelegram.fetch_message_id(message))

    return


def bot_help(update: Update, context: CallbackContext) -> None:
    """Bot help command"""

    update.message.reply_text("Help command not implemented, see Help following the buttons sent by /start")

    # remove /update message from user
    context.bot.delete_message(update.message.chat.id, update.message.message_id)

    return


def bot_update(update: Update, context: CallbackContext) -> None:
    """To download the last version of the messages"""

    ui.update_messages(sheet.get_dict_phrases())
    ui.update_buttons(sheet.get_dict_buttons())

    # remove /update message from user
    context.bot.delete_message(update.message.chat.id, update.message.message_id)

    return


def handle_message(update: Update, context: CallbackContext):
    id_telegram = mytelegram.fetch_id_telegram(update)
    l = sql.get_language(id_telegram)
    phone_number = mytelegram.fetch_phone_number(update, l)
    if phone_number is not "":
        sql.set_phone_number(id_telegram, phone_number)

        mytelegram.delete_message(id_telegram, update.message.reply_to_message.message_id)
        mytelegram.delete_message(id_telegram, update.message.message_id)

        mytelegram.send_main_message(id_telegram)

    return


# updater = Updater(os.environ["TEST_BOT_TOKEN"], use_context=True)
updater = Updater(os.environ["BOT_TOKEN"], use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', bot_start))
updater.dispatcher.add_handler(CommandHandler('help', bot_help))
updater.dispatcher.add_handler(CommandHandler('update', bot_update))

updater.dispatcher.add_handler(CallbackQueryHandler(menus.distribute_callback))

updater.dispatcher.add_handler(MessageHandler(None, handle_message))

setup()

print("start_polling")
updater.start_polling()
