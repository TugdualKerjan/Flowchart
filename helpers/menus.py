# author: Elior Papiernik (elior.papiernik@gmail.com)

import telegram
from telegram import Update

from . import ui

# === HELPERS ===


def edit_message_text(update: Update, message: str, markup) -> None:
    # query = update.callback_query
    # query.answer()
    print(type(message))
    update.callback_query.edit_message_text(
        text="message",
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN)

    return


def distribute_callback(update: Update, context):
    # query = update.callback_query
    # query.answer()

    stacktrace = update.callback_query.data.split(" ")

    # if stacktrace[0] in ui.special:
    #     pair = handle_special_callback(
    #         stacktrace, id_telegram, update, context)
    #     if pair is None:
    #         return
    #     keyboard = pair[0]
    #     message = pair[1]
    # else:
    keyboard = ui.build_keyboard_with_origin(stacktrace)
    message = stacktrace[0]  # rename
    print(str(type(message)) + " " + message)
    edit_message_text(update, message, keyboard)

    return


# def handle_special_callback(stacktrace: list, id_telegram, update, context):
#     keyboard = None
#     message = None

#     val = stacktrace[0]

#     if val in ui.message_on_cloud:
#         message = ui.message(stacktrace[0])
#         keyboard = ui.build_keyboard_only_back(stacktrace)

#     if message is None:
#         message = ui.message(stacktrace[0])
#     return keyboard, message
