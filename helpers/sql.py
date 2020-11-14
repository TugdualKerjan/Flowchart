# author: Elior Papiernik (elior.papiernik@gmail.com)

import mysql.connector
import os, math

from . import ui

try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass

cache_id_language = {}

all_lines = "*"

users = "users"
registrations = "registrations"

id = "id"
timestamp = "timestamp"

id_telegram = "id_telegram"
first_name = "first_name"
phone_number = "phone_number"
username = "username"
language = "language"
section = "section"
year = "year"
menu_id = "menu_id"

domain = "domain"
paired = "paired"

mydb = mysql.connector.connect(host=os.environ["DB_HOST"],
                               user=os.environ["DB_USER"],
                               passwd=os.environ["DB_PWD"],
                               db=os.environ["DB_USED"]
                               )


# mydb = mysql.connector.connect(host=os.environ["DB_HOST"],
#                                user=os.environ["DB_USER"],
#                                passwd=os.environ["DB_PWD"],
#                                db=os.environ["DB_USED"]
#                                )

# mycursor = mydb.cursor(buffered=True)


def reset_users() -> None:
    """Removes and recreates users table. To use upon setup"""

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("DROP TABLE IF EXISTS users")
    mycursor.execute("CREATE TABLE users "
                     "(id INT AUTO_INCREMENT PRIMARY KEY, "
                     "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "id_telegram INT, "
                     "first_name TEXT, "
                     "phone_number TEXT, "
                     "username TEXT, "
                     "language TEXT, "
                     "section TEXT, "
                     "year TEXT,"
                     "menu_id INT)")

    mycursor.close()

    return


def reset_registrations() -> None:
    """Removes and recreates registrations table. To use upon setup"""

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("DROP TABLE IF EXISTS registrations")
    mycursor.execute("CREATE TABLE registrations "
                     "(id INT AUTO_INCREMENT PRIMARY KEY, "
                     "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "id_telegram INT, "
                     "domain TEXT, "
                     "paired BOOLEAN DEFAULT FALSE)")

    mycursor.close()

    return


def reset_pairings():
    """Removes and recreates pairings table. To use upon setup"""

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("DROP TABLE IF EXISTS pairings")
    mycursor.execute("CREATE TABLE pairings "
                     "(id INT AUTO_INCREMENT PRIMARY KEY, "
                     "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "id_telegram INT, "
                     "id_telegram_partner INT, "
                     "id_message_contact INT,"
                     "is_username BOOLEAN)")

    mycursor.close()

    return


def print_users() -> None:
    """Displays all registered users"""

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()

    for r in myresult:
        print(r)

    mycursor.close()

    return


def register_user(id_telegram, first_name) -> None:
    """Registers a user with the given parameters"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "INSERT INTO users (id_telegram, first_name, language) VALUES (%s, %s, %s)"
    user = (id_telegram, first_name, ui.default_language)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def remove_user(id_telegram) -> None:
    """Unregisters a user from the database"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "DELETE FROM users WHERE id_telegram=%s"
    user = (id_telegram,)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    if id_telegram in cache_id_language:
        del cache_id_language[id_telegram]

    remove_registrations(id_telegram)

    mycursor.close()

    return


def set_username(id_telegram, username) -> None:
    """Adds the username of a user in the corresponding line of users table"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE users SET username=%s WHERE id_telegram=%s"
    user = (username, id_telegram)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def set_phone_number(id_telegram, phone_number) -> None:
    """Adds the phone number of a user in the corresponding line of users table"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE users SET phone_number=%s WHERE id_telegram=%s"
    user = (phone_number, id_telegram)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def set_language(id_telegram, language) -> None:
    """Updates the language of id_telegram user"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE users SET language=%s WHERE id_telegram=%s"
    user = (language, id_telegram)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    cache_id_language[id_telegram] = language

    mycursor.close()

    return


def set_section(id_telegram, section) -> None:
    """Updates the language of id_telegram user"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE users SET section=%s WHERE id_telegram=%s"
    user = (section, id_telegram)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def set_year(id_telegram, year) -> None:
    """Updates the language of id_telegram user"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE users SET year=%s WHERE id_telegram=%s"
    user = (year, id_telegram)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def set_menu_id(id_telegram, menu_id) -> None:
    """Updates the language of id_telegram user"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE users SET menu_id=%s WHERE id_telegram=%s"
    user = (menu_id, id_telegram)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def register_domain(id_telegram, domain):
    """Registers a user in the given domain"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "INSERT INTO registrations (id_telegram, domain) VALUES (%s, %s)"
    user = (id_telegram, domain)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def update_registration_courses(id_telegram, old_reg_courses, new_reg_courses):
    """Updates the eventual registrations of a user in the courses domain"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE registrations SET domain=%s WHERE id_telegram=%s AND domain=%s AND paired=%s"
    user = (new_reg_courses, id_telegram, old_reg_courses, False)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def remove_registration(id_telegram, domain):
    """Unregisters all user's registrations from the database"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "DELETE FROM registrations WHERE id_telegram=%s AND domain=%s AND paired=%s"
    user = (id_telegram, domain, False)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def remove_registrations(id_telegram):
    """Unregisters all user's registrations from the database"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "DELETE FROM registrations WHERE id_telegram=%s"
    user = (id_telegram,)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def pair_validation(id_telegram, domain):
    """Updates the paired field of id_telegram user"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "UPDATE registrations SET paired=%s WHERE id_telegram=%s AND domain=%s AND paired=%s"
    user = (True, id_telegram, domain, False)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def add_pairing(tg_id, tg_id_partner, id_message, is_username) -> None:
    """Adds a pairing with the given parameters"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "INSERT INTO pairings (id_telegram, id_telegram_partner, id_message_contact, is_username) VALUES (%s, %s, %s, %s)"
    user = (tg_id, tg_id_partner, id_message, is_username)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return


def remove_all_pairings_of_user(tg_id):
    """Removes all user's pairings from the table"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "DELETE * FROM pairings WHERE id_telegram=%s OR id_telegram_partner=%s"
    user = (tg_id, tg_id)

    mycursor.execute(sql_formula, user)
    mydb.commit()

    mycursor.close()

    return



def print_all() -> None:
    """Test purpose, to remove"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "SELECT language FROM users WHERE id_telegram=%s"
    user = (658414959,)

    mycursor.execute(sql_formula, user)

    language = mycursor.fetchone()

    mycursor.close()

    return


def reset_user(id_telegram):
    set_language(id_telegram, ui.default_language)
    set_section(id_telegram, None)
    set_year(id_telegram, None)

    return


def get_all(database, column, key_condition, value_condition, args=""):
    """Returns all occurences of a field with key condition from given database"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "SELECT " + column + " FROM " + database + " WHERE " + key_condition + "=%s" + args
    params = (value_condition,)

    mycursor.execute(sql_formula, params)

    value = mycursor.fetchall()

    mycursor.close()

    return sql_one_to_list(value)


def get_one(database, column, key_condition, value_condition, args=""):
    """Returns one occurence of a field with key condition from given database"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "SELECT " + column + " FROM " + database + " WHERE " + key_condition + "=%s" + args
    params = (value_condition,)

    mycursor.execute(sql_formula, params)

    value = mycursor.fetchone()

    mycursor.close()

    return value if value is None else value[0]


def get_one_from_users(column, key_condition, value_condition):
    return get_one(users, column, key_condition, value_condition)


def get_one_from_registrations(column, key_condition, value_condition):
    return get_one(registrations, column, key_condition, value_condition)


def get_all_from_users(column, key_condition, value_condition):
    return get_all(users, column, key_condition, value_condition)


def get_all_from_registrations(column, key_condition, value_condition):
    return get_all(registrations, column, key_condition, value_condition)


def get_one_from_users_with_id_telegram(column, value_condition):
    return get_one_from_users(column, id_telegram, value_condition)


def get_one_from_registrations_with_id_telegram(column, value_condition):
    return get_one_from_registrations(column, id_telegram, value_condition)


def get_all_from_users_with_id_telegram(column, value_condition):
    return get_all_from_users(column, id_telegram, value_condition)


def get_all_from_registrations_with_id_telegram(column, value_condition):
    return get_all_from_registrations(column, id_telegram, value_condition)


def get_section(tg_id):
    """Returns a users' section

        The pair (id_telegram: section) will be fetched from database added to the cache is not already present in the cache
    """

    s = get_one_from_users_with_id_telegram(section, tg_id)

    return s


def get_year(tg_id):
    """Returns a users' year"""

    y = get_one_from_users_with_id_telegram(year, tg_id)

    return y


def get_language(tg_id):
    """Returns a users' language

        The pair (id_telegram: language) will be fetched from database added to the cache is not already present in the cache
    """

    if tg_id in cache_id_language:
        return cache_id_language[tg_id]
    else:
        l = get_one_from_users_with_id_telegram(language, tg_id)
        cache_id_language[tg_id] = l

        return l


def get_username(tg_id):
    """Returns a users' username"""

    u = get_one_from_users_with_id_telegram(username, tg_id)

    return u


def get_first_name(tg_id):
    """Returns a users' first name"""

    f = get_one_from_users_with_id_telegram(first_name, tg_id)

    return f


def get_menu_id(tg_id):
    """Returns a users' first name"""

    m = get_one_from_users_with_id_telegram(menu_id, tg_id)

    return m


def exist_user(tg_id) -> bool:
    """Returns True if user with given id_telegram is already in database users, False otherwise"""

    user = get_one_from_users_with_id_telegram(all_lines, tg_id)

    return False if user is None else True


def get_registrations(domain_name):
    """Returns all telegram_ids of users registered to the given domain"""

    regs = get_all(registrations, id_telegram, domain, domain_name, " AND " + paired + "=0")

    return regs


def get_registered(tg_id, domain_name) -> bool:
    """Returns True if tg_id is registered to domain_name, False otherwise"""

    regs = get_registrations(domain_name)
    for reg in regs:
        if reg == tg_id:
            return True

    return False


def get_all_pairings_of_user(tg_id):
    """Returns all pairings of a user"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "SELECT * FROM pairings WHERE id_telegram=%s OR id_telegram_partner=%s"
    params = (tg_id, tg_id)

    mycursor.execute(sql_formula, params)

    value = mycursor.fetchall()

    mycursor.close()

    return sql_many_to_list(value)


def sql_one_to_list(args):
    same_list = []

    for arg in args:
        same_list.append(arg[0])

    return same_list


def sql_many_to_list(args):
    same_list = []

    for arg in args:
        t = []
        for a in arg:
            t.append(a)
        same_list.append(t)

    return same_list


def get_nb_users():
    """Returns number of users"""

    mycursor = mydb.cursor(buffered=True)

    sql_formula = "SELECT COUNT(*) FROM users"

    mycursor.execute(sql_formula)

    value = mycursor.fetchone()

    mycursor.close()

    return value[0]


def get_nb_pairings_domain(domain):
    """Returns number of users"""

    mycursor = mydb.cursor(buffered=True)

    if domain == ui.courses:
        sql_formula = "SELECT domain FROM registrations WHERE paired=%s"
        user = (True,)

        mycursor.execute(sql_formula, user)

        value = mycursor.fetchall()
        result = 0
        for val in sql_one_to_list(value):
            if domain in val:
                result += 1

    else:

        sql_formula = "SELECT COUNT(*) FROM registrations WHERE paired=%s AND domain=%s"
        user = (True,domain)

        mycursor.execute(sql_formula, user)

        value = mycursor.fetchone()
        result = value[0]

    mycursor.close()

    return math.ceil(result/2)


"""
reset_users()
register_user(456, "Papiernik")
register_user(658414959, "Elior")
register_user(123, "TOTO")
add_username(123, "@Elior")
unregister_user(658414959)
print(exist_user(658414959))
add_phone_number(456, "+33695033268")
print_users()
"""
