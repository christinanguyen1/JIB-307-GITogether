import sqlite3
imprt

# tag error classes


class TagError:
    pass


class ClubDoesNotExist(TagError):
    pass


class MalformedTag(TagError):
    pass

# TAG-based search API


class TagMachine:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.db = self.conn.cursor()

    def get_club_tags(club_name, tags):
        for tag in tags:
            if (' ' in tag):
                raise MalformedTag
            else:
                insert_into_db_table("club", "tags", tag)
        pass

    def add_club_tags():
        pass

    def clear_club_tags():
        pass

    def remove_club_tags():
        pass

    def search_club_by_tags():
        pass
