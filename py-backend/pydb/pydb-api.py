# an API for GITogether DB operations
# @author: owenns

import re
import sqlite3

# error classes


class InvalidEmailError(Error):
    pass


class InvalidPasswordError(Error):
    pass


class NoSuchUserFoundError(Error):
    pass


class IncorrectPasswordError(Error):
    pass


class UserAlreadyRegisteredError(Error):
    pass

# helper functions


def contains_digits(d):
    _digits = re.compile('\d')
    return bool(_digits.search(d))


def contains_alpha(a):
    _alpha_chars = re.compile('[a-z][A-Z]')
    return bool(_alpha_chars.search(a))


def is_len(min_size, st):
    return len(str(st)) >= min_size


def db_table_exists(conn, table_name):
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        c.close()
        return True
    else:
        c.close()
        return False


# (API CALL) for registering a new user
# email, password must be a tuple data type (sanitization)


def new_user_db((email, password)):
    if "@" not in email and "." not in email:
        print("invalid email: must include @ and .<domain>")
        raise InvalidEmailError
    if not contains_alpha(password) or not contains_digits(password) or not is_len(8, password):
        print("invalid password: must be at least 8 characters long and contain at least one letter and digit")
        raise InvalidPasswordError

    conn = sqlite3.connect('gitogether_db')
    if db_table_exists(conn, 'user_login'):
        c = conn.cursor()
        login = (email, password)
        c.execute('INSERT INTO user_login VALUES (?)', login)

        conn.commit()
        conn.close()

        return True
    else:
        c = conn.cursor()
        login = (email, password)

        # create table if not already made
        # hash passwords later
        c.execute('''CREATE TABLE user_login (email text, password text)''')
        c.execute('INSERT INTO user_login VALUES (?)', login)

        conn.commit()
        conn.close()
        return True
    return False
