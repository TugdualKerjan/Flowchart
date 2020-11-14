# author: Elior Papiernik (elior.papiernik@gmail.com)

from . import sql, mytelegram


def get_pair(id_telegram: int, domain: str) -> int:
    """Returns the id of the user to be paired with and 0 if does not exist"""

    registrations = sql.get_registrations(domain)
    for reg in registrations:
        if reg != id_telegram:
            return reg
    return 0


def pair_actions(domain, id_1, id_2):
    mytelegram.send_contact(sql.get_language(id_1), domain, id_1, id_2)
    mytelegram.send_contact(sql.get_language(id_2), domain, id_2, id_1)
    update_one(id_1, domain)
    update_one(id_2, domain)

    return


def update_one(id_telegram, domain):
    sql.pair_validation(id_telegram, domain)
    mytelegram.delete_message(id_telegram, sql.get_menu_id(id_telegram))
    mytelegram.send_main_message(id_telegram)

    return


# def make_pair(id_1, id_2, domain):
#     mytelegram.send_contact(id_)
