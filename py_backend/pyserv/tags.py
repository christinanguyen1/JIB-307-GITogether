import sqlite3

# tag error classes


class TagError:
    pass


class ClubDoesNotExist(TagError):
    pass


class MalformedTag(TagError):
    pass

# TAG-based search API

# the tag machine is given the database to work on
# useage should be to create a TagMachine object `tagm = TagMachine('gitogether.db')`
# and then use `del tagm` when done with operations

# tags should be comma separated values ex. "pro,wrestling,match,club,watch"


class TagMachine:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.db = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_club_tags(club_name, tags):
        pass

    def add_club_tags():
        pass

    def clear_club_tags():
        pass

    def remove_club_tags():
        pass

    def search_club_by_tags():
        pass
