# author: Elior Papiernik (elior.papiernik@gmail.com)

import os

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler

from helpers import mytelegram
from helpers import ui
from helpers import menus

from spreadsheet import sheet


def bot_start(update: Update, context: CallbackContext) -> None:
    """Bot start command"""

    message = update.message.reply_text(ui.message(ui.start, l),
                                        reply_markup=ui.build_keyboard_start(
                                            l, ui.languages_layout),
                                        parse_mode=telegram.ParseMode.MARKDOWN)

    return


# def handle_message(update: Update, context: CallbackContext):
#     id_telegram = mytelegram.fetch_id_telegram(update)
#     l = sql.get_language(id_telegram)
#     phone_number = mytelegram.fetch_phone_number(update, l)
#     if phone_number is not "":
#         sql.set_phone_number(id_telegram, phone_number)

#         mytelegram.delete_message(
#             id_telegram, update.message.reply_to_message.message_id)
#         mytelegram.delete_message(id_telegram, update.message.message_id)

#         mytelegram.send_main_message(id_telegram)

#     return

updater = Updater(os.environ["BOT_TOKEN"], use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', bot_start))

updater.dispatcher.add_handler(CallbackQueryHandler(menus.distribute_callback))

# updater.dispatcher.add_handler(MessageHandler(None, handle_message))

print("Started pool")
updater.start_polling()
