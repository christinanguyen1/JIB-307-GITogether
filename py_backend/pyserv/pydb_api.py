# an API for GITogether DB operations
# @author: owenns

import re
import sqlite3
import bcrypt

# error classes


class InvalidEmailError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class NoSuchUserFoundError(Exception):
    pass


class EmailNotFoundError(Exception):
    pass


class IncorrectLoginError(Exception):
    pass


class UserAlreadyRegisteredError(Exception):
    pass


class PasswordNotMatched(Exception):
    pass


class UnknownError(Exception):
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
    if c.fetchone() is not None:
        # print('fetch one works')
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
    result = c.fetchone()
    if result[0] > 0:
        c.close()
        return True
    else:
        c.close()
        return False

# bcrypt API tools (for password hashing)


def hash_password(plaintext_pass):
    return plaintext_pass
    #pass_bytes = plaintext_pass.encode("utf-8")
    # hash password with a randomly generated salt
    #cyphertext_pass = bcrypt.hashpw(pass_bytes, bcrypt.gensalt())
    # return cyphertext_pass


def check_hash_password(plaintext_pass, cyphertext_pass):
    return plaintext_pass == cyphertext_pass
    # print("check: plain: " + str(plaintext_pass) +
    #       "stored: " + str(cyphertext_pass))
    # plain_pass_bytes = plaintext_pass.encode("utf-8")
    # cypher_pass_bytes = cyphertext_pass.encode("utf-8")
    # return bcrypt.checkpw(plain_pass_bytes, cypher_pass_bytes)

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
        # need to hash password and then insert into DB
        cyphertext_pass = str(hash_password(password))
        c.execute('INSERT INTO user_login VALUES (?,?)',
                  (email, cyphertext_pass))

        print("inserted (" + str(email) + ", " +
              password + ", " + cyphertext_pass + ")")

        conn.commit()
        conn.close()

        return True
    else:
        c = conn.cursor()

        # create table if not already made
        # hash passwords later
        c.execute('''CREATE TABLE user_login (email text, password text)''')
        # need to hash password and then insert into DB
        cyphertext_pass = str(hash_password(password))
        c.execute('INSERT INTO user_login VALUES (?,?)',
                  (email, cyphertext_pass))

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

    c.execute('SELECT * FROM user_login WHERE email=?',
              (email,))

    result = c.fetchone()

    if result == None:
        print("incorrect email: not found in db")
        raise EmailNotFoundError

    conn.close()

    db_password = result[1]
    return check_hash_password(password, db_password)

# (API CALL) for finding if email exists in database for forgot
# email is string and returns a string with the password and a message


def forgot_email(email):
    conn = sqlite3.connect('gitogether.db')
    c = conn.cursor()
    cmd_str = "SELECT password FROM user_login WHERE email='{0}'".format(email)
    c.execute(cmd_str)
    result = c.fetchone()
    if result is None:
        raise InvalidEmailError
    return result

# -------------------------------------------
# API PRIMITIVE CALLS (USE WITH CAUTION)
# -------------------------------------------

# select information from tables and insert from tables


class PrimitiveError:
    pass


class CreateTableError(PrimitiveError):
    pass


class InsertTableError(PrimitiveError):
    pass


class SelectTableError(PrimitiveError):
    pass

# the kv_pairs MUST be 1-1 (each key only has one value)
# ex. CREATE TABLE dnd_table (name text, class test, level real)
# @param db_name is the name of the database you want to make the table in ex. "gitogether.db"
# @param table_name would be dnd_table
# @param kv_pairs would be {'name':'text', 'class':'text', 'level':'real'}
# @param debug - True if you want debugging on, false otherwise


def create_db_table(db_name: str, table_name: str, kv_pairs: dict, debug: bool):
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
    return True


# ex. dnd_table with attributes (name text, class test, level real)
# ex. INSERT INTO dnd_table VALUES ('storm silverhand', 'bard', '27')
# @param db_name is the name of the database you want to make the table in ex. "gitogether.db"
# @param table_name would be dnd_table
# @param list would be ['storm silverhand', 'bard', '27']
# @param debug - True if you want debugging on, false otherwise
def insert_into_db_table(db_name: str, table_name: str, values: list, debug: bool):
    cmd_str = "INSERT INTO {0} VALUES (".format(table_name)
    val_count = 0
    for value in values:
        if val_count != len(values) - 1:
            val_str = "\'{0}\',".format(str(value))
            if debug:
                print("parsed insert value: " + val_str)
            cmd_str = cmd_str + val_str
        else:
            val_str = "\'{0}\'".format(str(value))
            if debug:
                print("parsed insert value: " + val_str)
            cmd_str = cmd_str + val_str
        val_count += 1
    if debug:
        print("INSERT_INTO_DB_TABLE cmd_str: {0}".format(cmd_str))
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(cmd_str)
    conn.commit()
    conn.close()
    return True


def insert_into_club_table(name: str, desc: str, rec: str):
    conn = sqlite3.connect('gitogether.db')
    c = conn.cursor()
    # cmd_str = "INSERT INTO clubs (club_name, club_description, club_recruitment) VALUES ('{0}', '{1}', '{2}')".format(name, desc, rec)
    # print(cmd_str)
    c.execute('INSERT INTO clubs (club_name, club_description, club_recruitment) VALUES (?,?,?)', (name, desc, rec))
    # c.execute(cmd_str)
    conn.commit()
    conn.close()
    print("success of adding club")

# ex. dnd_table with attributes (name text, class test, level real)
# ex. 'SELECT * FROM dnd_table WHERE class=ranger
# @param db_name is the name of the database you want to make the table in ex. "gitogether.db"
# @param table_name would be dnd_table
# @param selector would be '*'
# @param where would be 'class=ranger' or 'class=ranger AND level=3'
# @param debug - True if you want debugging on, false otherwise
# @returns a list of rows from the query, if any. errors when stuff goes bad


def select_from_db_table(db_name: str, table_name: str, selector: str, where: str, debug: str):
    cmd_str = "SELECT {0} FROM {1} WHERE {2}".format(
        table_name, selector, where)
    if debug:
        print("SELECT_FROM_DB_TABLE cmd_str: {0}".format(cmd_str))
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(cmd_str)
    return_row_list = []
    for row in c.fetchall():
        return_row_list.append(row)
    conn.close()
    return return_row_list


def render_clubs_homepage():
    conn = sqlite3.connect('gitogether.db')
    c = conn.cursor()
    c.execute('SELECT club_name, club_description FROM clubs')
    items = c.fetchall()
    return items


def render_clubs_clubpage(variable):
    # implement for the club pages
    conn = sqlite3.connect('gitogether.db')
    c = conn.cursor()
    c.execute(
        "SELECT club_name, club_description, club_recruitment FROM clubs WHERE club_name = '{0}'".format(variable))
    items = c.fetchall()
    return items
