# an API for GITogether DB operations
# @author: owenns

import re
import sqlite3

# error classes


class Error:
    pass


class InvalidEmailError(Error):
    pass


class InvalidPasswordError(Error):
    pass


class NoSuchUserFoundError(Error):
    pass


class IncorrectLoginError(Error):
    pass


class UserAlreadyRegisteredError(Error):
    pass


class PasswordNotMatched(Error):
    pass


class UnknownError(Error):
    pass

# helper functions


def contains_digits(d):
    _digits = re.compile('\d')
    return bool(_digits.search(d))


def contains_alpha(a):
    _alpha_chars = re.compile('[a-zA-Z]*')
    return bool(_alpha_chars.search(a))


def is_len(min_size, st):
    return len(str(st)) >= min_size


def db_table_exists(conn, table_name):
    c = conn.cursor()
    c.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ''', (table_name,))
    if c.fetchone()[0] == 1:
        c.close()
        return True
    else:
        c.close()
        return False


def db_row_exists(conn, table_name, attribute, value):
    c = conn.cursor()
    cmd_str = "SELECT count(*) FROM {0} WHERE {1}=\"{2}\"".format(
        table_name, attribute, str(value))
    c.execute(cmd_str)
    if c.fetchone()[0] > 1:
        c.close()
        return True
    else:
        c.close()
        return False


# (API CALL) for registering a new user
# email, password must be a tuple data type (sanitization)


def new_user_db(login_tuple):
    if len(login_tuple) > 3:
        print("invalid login tuple: correct form is (username, password)")
        raise IncorrectLoginError
    email = login_tuple[0]
    password = login_tuple[1]
    confirm_password = login_tuple[2]
    if "@" not in email and "." not in email:
        print("invalid email: must include @ and .<domain>")
        raise InvalidEmailError
    if not contains_alpha(password) or not contains_digits(password) or not is_len(8, password):
        print("invalid password: must be at least 8 characters long and contain at least one letter and digit")
        raise InvalidPasswordError
    if password != confirm_password:
        print("password and confirmed password must match!")
        raise PasswordNotMatched

    conn = sqlite3.connect('gitogether.db')
    if db_table_exists(conn, 'user_login'):

        if db_row_exists(conn, "user_login", "email", email):
            print("user already exists")
            raise UserAlreadyRegisteredError

        c = conn.cursor()
        c.execute('INSERT INTO user_login VALUES (?,?)', (email, password))

        conn.commit()
        conn.close()

        return True
    else:
        c = conn.cursor()

        # create table if not already made
        # hash passwords later
        c.execute('''CREATE TABLE user_login (email text, password text)''')
        c.execute('INSERT INTO user_login VALUES (?,?)', (email, password))

        conn.commit()
        conn.close()
        return True
    return False

# (API CALL) for logging a user in
# email, password must be a tuple data type (sanitization)


def check_login_db(login_tuple):
    if len(login_tuple) > 2:
        print("invalid login tuple: correct form is (username, password)")
        raise IncorrectLoginError
    email = login_tuple[0]
    password = login_tuple[1]
    conn = sqlite3.connect('gitogether.db')
    if not db_table_exists(conn, "user_login"):
        print("table not found")
        raise UnknownError
    c = conn.cursor()

    c.execute('SELECT * FROM user_login WHERE email=? AND password=?',
              (email, password))
    result = c.fetchone()
    row_count = c.rowcount

    if row_count == 0:
        print("incorrect email/password combination; try again")
        raise IncorrectLoginError
    return True

# -------------------------------------------
# API PRIMITIVE CALLS (USE WITH CAUTION)
# -------------------------------------------

# select information from tables and insert from tables


class PrimitiveError:
    pass


class CreateTableError(PrimitiveError):
    pass


# the kv_pairs MUST be 1-1 (each key only has one value)
# ex. CREATE TABLE dnd_table (name text, class test, level real)
# @param is the name of the database you want to make the table in ex. "gitogether.db"
# @param table_name would be dnd_table
# @param kv_pairs would be {'name':'text', 'class':'text', 'level':'real'}
# @param debug - True if you want debugging on, false otherwise
def create_db_table(db_name, table_name, kv_pairs: dict, debug):
    cmd_str = "CREATE TABLE {0} (".format(table_name)
    attr_counter = 0
    for key, value in kv_pairs.items():
        if len(value) != 1:
            if debug:
                print("incorrect usage of kv_pair; see function comments")
            raise CreateTableError
        else:
            if attr_counter != len(kv_pairs.keys()) - 1:
                attr_str = "{0} {1},".format(key, value)
            else:
                attr_str = "{0} {1}".format(key, value)
            if debug:
                print("parsed table attributes: " + attr_str)
            cmd_str = cmd_str + attr_str
        attr_counter += 1
    cmd_str = cmd_str + ")"
    if debug:
        print("CREATE_DB_TABLE cmd_str: {0}".format(cmd_str))
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(cmd_str)
    conn.commit()
    conn.close()
