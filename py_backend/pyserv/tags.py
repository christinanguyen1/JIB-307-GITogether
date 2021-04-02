import sqlite3

# tag error classes


class TagError(Exception):
    pass


class ClubDoesNotExist(Exception):
    pass


class TagDoesNotExist(Exception):
    pass


class MalformedTag(Exception):
    pass

# TAG-based search API

# the tag machine is given the database to work on
# useage should be to create a TagMachine object `tagm = TagMachine('gitogether.db')`
# and then use `del tagm` when done with operations


class TagMachine:

    def __init__(self, database: str):
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

    def remove_tag_occurrance(self, taglist: list, target: str):
        try:
            taglist.remove(target)
        except Exception as e:
            print("tried to remove a tag that never existed: " + target)
            raise TagDoesNotExist

    def remove_all_tag_occurrances(self, taglist: list, target: str):
        while target in taglist:
            self.remove_tag_occurrance(taglist, target)

    def get_club_tags(self, club_name: str):
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

    def remove_club_tags(self, club_name: str, tags_to_remove: list):
        current_tags = self.get_club_tags(club_name)
        for tag in tags_to_remove:
            self.remove_all_tag_occurrances(current_tags, tag)
        self.add_club_tags(club_name, current_tags)

    def search_club_by_tags():
        pass
