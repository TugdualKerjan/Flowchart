# author: Elior Papiernik (elior.papiernik@gmail.com)

import os

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler

from helpers import ui
from helpers import menus

start_message = "Welcome to this bot!"

# Start command
def bot_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(start_message,
                                        reply_markup=ui.build_keyboard_with_origin(["menu"]),
                                        parse_mode=telegram.ParseMode.MARKDOWN)

    # return

# updater = Updater(os.environ["BOT_TOKEN"], use_context=True)
updater = Updater("1479755779:AAERf2hlxLUzXAVzkmopuZLPMba9wX7fo68", use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', bot_start))

updater.dispatcher.add_handler(CallbackQueryHandler(menus.distribute_callback))

print("Started pool")
updater.start_polling()
