# author: Elior Papiernik (elior.papiernik@gmail.com)

import telegram
from telegram import Update

from . import ui, sql, mytelegram, pairing


# === HELPERS ===

def edit_message_text(update: Update, message, markup) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=message,
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN)

    return


def distribute_callback(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    id_telegram = mytelegram.fetch_id_telegram(update)
    l = sql.get_language(id_telegram)

    stacktrace = data.split(" ")

    if stacktrace[0] in ui.special:
        pair = handle_special_callback(l, stacktrace, id_telegram, update, context)
        if pair is None:
            return
        keyboard = pair[0]
        message = pair[1]
    else:
        keyboard = ui.build_keyboard_with_origin(l, stacktrace, ui.menus_layout[stacktrace[0]])
        message = ui.message(stacktrace[0], sql.get_language(id_telegram))
    edit_message_text(update, message, keyboard)

    return


def handle_special_callback(l, stacktrace: list, id_telegram, update, context):
    keyboard = None
    message = None

    val = stacktrace[0]

    if val == ui.start:
        l = stacktrace[1]
        sql.set_language(id_telegram, stacktrace[1])
        message = ui.message(ui.share_contact, l)
        keyboard = ui.build_keyboard_share_contact(l, ui.menus_layout[ui.share_contact])

    elif val == ui.share_contact:
        keyboard = ui.build_keyboard_share_contact(l, ui.menus_layout[ui.share_contact])

    elif val == ui.share_username:
        username = mytelegram.fetch_username(update)
        if username is None:
            message = ui.message(ui.share_username, l)
            keyboard = ui.build_keyboard_share_contact(l, ui.menus_layout[ui.share_contact])
            # TODO ajouter un compteur du nombre de tentatives échouées
        else:
            sql.set_username(id_telegram, username)
            message = ui.message(ui.main, l)
            keyboard = ui.build_keyboard_with_origin(l, [ui.main])

    elif val == ui.share_phone_number:
        mytelegram.delete_message(id_telegram, sql.get_menu_id(id_telegram))
        reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(ui.buttons_menu[ui.ask_phone_or_cancel][l], request_contact=True)]])
        context.bot.sendMessage(mytelegram.fetch_id_telegram(update), ui.message(ui.ask_phone_or_cancel, l), reply_markup=reply_markup)

    # elif val == ui.create_username:
    #     keyboard = ui.build_keyboard_check_param(l, stacktrace)

    elif val == ui.language:
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.languages, l, ui.menus_layout[ui.language])

    elif val in ui.languages:
        sql.set_language(id_telegram, val)
        stacktrace.pop(0)
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.languages, val, ui.menus_layout[ui.language])

    elif val == ui.section:
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.sections, sql.get_section(id_telegram), ui.menus_layout[ui.section])

    elif val in ui.sections:
        section = sql.get_section(id_telegram)
        year = sql.get_year(id_telegram)
        sql.set_section(id_telegram, val)
        if section and year:
            old_reg_courses = ui.courses + section + year
            new_reg_courses = ui.courses + val + year
            sql.update_registration_courses(id_telegram, old_reg_courses, new_reg_courses)
        stacktrace.pop(0)
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.sections, val, ui.menus_layout[ui.section])

    elif val == ui.year:
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.years, sql.get_year(id_telegram), ui.menus_layout[ui.year])

    elif val in ui.years:
        section = sql.get_section(id_telegram)
        year = sql.get_year(id_telegram)
        sql.set_year(id_telegram, val)
        if section and year:
            old_reg_courses = ui.courses + section + year
            new_reg_courses = ui.courses + val + year
            sql.update_registration_courses(id_telegram, old_reg_courses, new_reg_courses)
        stacktrace.pop(0)
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.years, val, ui.menus_layout[ui.year])

    elif val == ui.data:
        keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.datas)

    elif val in ui.datas:
        if val == ui.del_all:
            sql.reset_user(id_telegram)
            sql.remove_registrations(id_telegram)
            message = ui.message(ui.start, ui.default_language)
            keyboard = ui.build_keyboard_start(ui.default_language, ui.menus_layout[ui.language])
        elif val == ui.forget:
            mytelegram.user_quits(id_telegram, l)
            sql.remove_user(id_telegram)
            return

    elif val in ui.message_on_cloud:
        message = ui.message(stacktrace[0], l)
        keyboard = ui.build_keyboard_only_back(l, stacktrace)

    elif val == ui.courses:
        if sql.get_section(id_telegram) is None:
            keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.sections, sql.get_section(id_telegram), ui.menus_layout[ui.section])
        elif sql.get_year(id_telegram) is None:
            keyboard = ui.build_keyboard_check_param(l, stacktrace, ui.years, sql.get_year(id_telegram), ui.menus_layout[ui.year])
        else:
            keyboard = ui.build_keyboard_registration(l, stacktrace, sql.get_registered(id_telegram, ui.courses + sql.get_section(id_telegram) + sql.get_year(id_telegram)))

    elif val in ui.regable_menus:
        keyboard = ui.build_keyboard_registration(l, stacktrace, sql.get_registered(id_telegram, stacktrace[0]))

    elif val in ui.reg_buttons:
        domain = stacktrace[1]
        # To add section and year to the academic registration
        if domain == ui.courses:
            domain += sql.get_section(id_telegram) + sql.get_year(id_telegram)
        if val == ui.reg_button:
            sql.register_domain(id_telegram, domain)
            id_pair = pairing.get_pair(id_telegram, domain)
            if id_pair != 0:
                pairing.pair_actions(domain, id_telegram, id_pair)
                return
        else:
            sql.remove_registration(id_telegram, domain)
        stacktrace.pop(0)
        keyboard = ui.build_keyboard_registration(l, stacktrace, sql.get_registered(id_telegram, domain))

    elif val == ui.stats:
        message = ui.stats_message(l)
        keyboard = ui.build_keyboard_only_back(l, stacktrace)

    if message is None:
        message = ui.message(stacktrace[0], sql.get_language(id_telegram))
    return keyboard, message
