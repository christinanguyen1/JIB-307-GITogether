# PoC (proof of concept) for SQLite3 DB in Python
# @author: owens

import sqlite3


def test_populate_db():
    # connect to db
    conn = sqlite3.connect('py_test.db')
    c = conn.cursor()

    # create a new table dnd_table
    c.execute('''CREATE TABLE dnd_table (name text, class test, level real)''')
    # insert into dnd_table
    c.execute("INSERT INTO dnd_table VALUES ('drizzt do''urden', 'ranger', '30')")
    c.execute("INSERT INTO dnd_table VALUES ('storm silverhand', 'bard', '27')")
    c.execute(
        "INSERT INTO dnd_table VALUES ('bruenor battlehammer', 'fighter', '12')")

    # save changes to db
    conn.commit()

    # close connection
    conn.close()


def test_select_db():
    conn = sqlite3.connect('py_test.db')
    c = conn.cursor()

    # get a single row
    # IMPORTANT: santize strings before you query them; don't just use python's built-in string type as input
    single_query = ('ranger',)
    c.execute('SELECT * FROM dnd_table WHERE class=?', single_query)
    print("query results for \'ranger\':")
    print(c.fetchone())

    # get the whole table
    c.execute('SELECT * FROM dnd_table')
    print("query results for selecting entire dnd_table:")
    for row in c.fetchall():
        print(row)

    conn.close()


def test_delete_update_db():
    conn = sqlite3.connect('py_test.db')
    c = conn.cursor()

    del_query = ('fighter',)
    c.execute('DELETE FROM dnd_table WHERE class=?', del_query)
    update_query = ('johnny silverhand', 'bard',)
    c.execute('UPDATE dnd_table SET name=? WHERE class=?', update_query)

    conn.commit()
    conn.close()


def test_nuke_db():
    # WARNING: tests a DROP table function
    # will delete entire table; test_populate_db() must be run to test after
    conn = sqlite3.connect('py_test.db')
    c = conn.cursor()
    c.execute('DROP TABLE dnd_table')

    conn.commit()
    conn.close()


def menu():
    print("thanks for using the pydb tester! please enter in a selection")
    print("(1) populate test database\n(2) select test database\n(3) delete/update test database\n(4) drop test database (drop table)\n(5) quit")
    while True:
        selection = int(input(">"))
        if selection == 1:
            test_populate_db()
            print("populated test db successfully")
        if selection == 2:
            test_select_db()
        if selection == 3:
            test_delete_update_db()
            print("modified/delete test db successfully")
        if selection == 4:
            test_nuke_db()
            print("dropped test db table successfully")
        if selection == 5:
            break


menu()
