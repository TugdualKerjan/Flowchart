# author: Elior Papiernik (elior.papiernik@gmail.com)

import os

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler
import ui

start_message = "Welcome to this bot!"


def edit_message_text(update: Update, message: str, markup) -> None:
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN)


def distribute_callback(update: Update, context):
    keyboard = ui.build_keyboard_with_origin(update.callback_query.data)
    message = "a"*len(update.callback_query.data)  # rename
    edit_message_text(update, message, keyboard)


def bot_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(start_message,
                              reply_markup=ui.build_keyboard_with_origin("0"),
                              parse_mode=telegram.ParseMode.MARKDOWN)


updater = Updater(
    "1479755779:AAERf2hlxLUzXAVzkmopuZLPMba9wX7fo68", use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', bot_start))

updater.dispatcher.add_handler(CallbackQueryHandler(distribute_callback))

print("Started pool")
updater.start_polling()
