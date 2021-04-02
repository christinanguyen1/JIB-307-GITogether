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


class TagMachine:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.db = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def taglist_to_db_format(self, tags: list):
        db_form = ""
        last = len(tags) - 1
        for i, tag in enumerate(tags):
            if i == last:
                db_form = db_form + str(tag)
            else:
                db_form = db_form + str(tag) + ","
        return db_form

    def db_format_to_taglist(self, tagstr: str):
        return tagstr.split(',')

    def get_club_tags(self, club_name):
        self.db.execute(
            "SELECT tag_list from tags WHERE club_name = '{0}'".format(variable))
        club_tags = self.db.fetchone()
        if not club_tags:
            raise ClubDoesNotExist
        tag_list = self.db_format_to_taglist(club_tags[1])
        return tag_list

    # new_tags should be given as a list of strings ex. ["underwater", "basket", "weaving"]
    def add_club_tags(self, club_name: str, new_tags: list):
        tag_db_form = self.taglist_to_db_format(new_tags)
        self.db.execute("INSERT or REPLACE INTO tags (club_name, tag_list) VALUES ('{0}', '{1}');".format(
            club_name, tag_db_form))
        self.conn.commit()
        return True

    def clear_club_tags(self, club_name: str):
        self.db.execute(
            "INSERT or REPLACE INTO tags (club_name, tag_list) VALUES ('{0}', '');".format(club_name))
        self.conn.commit()
        pass

    def remove_club_tags():

        pass

    def search_club_by_tags():
        pass
