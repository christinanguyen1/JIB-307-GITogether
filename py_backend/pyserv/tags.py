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
            "SELECT tag_list FROM tags WHERE club_name = '{0}'".format(club_name))
        club_tags = self.db.fetchone()
        if not club_tags:
            raise ClubDoesNotExist
        tag_list = self.db_format_to_taglist(club_tags[0])
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
        new_tags = self.taglist_to_db_format(current_tags)
        self.db.execute("UPDATE tags SET tag_list = '{0}' WHERE club_name = '{1}'".format(
            new_tags, club_name))
        self.conn.commit()

    # returns list of clubs matching the tags; returns empty list if none are found
    def search_club_by_tags(self, key_tags: list):
        result_list = list()
        self.db.execute("SELECT * FROM tags")
        all_clubs = self.db.fetchall()
        for club in all_clubs:
            club_tag_list = self.db_format_to_taglist(club[1])
            for key in key_tags:
                if key in club_tag_list:
                    result_list.append(club[0])
        return result_list

# tests tag functionality


def test_tags():
    tagm = TagMachine('tagtest.db')

    clubs = [("Dungeons and Dragons", ["tabletop", "roleplaying", "game", "dragon", "test"]),
             ("AEW Fan Club", ["aew", "wrestling", "watch", "test"])]
    # test adding
    tagm.add_club_tags(clubs[0][0], clubs[0][1])
    tagm.add_club_tags(clubs[1][0], clubs[1][1])

    # test getting
    print("after adding:")
    print(tagm.get_club_tags(clubs[0][0]))
    print(tagm.get_club_tags(clubs[1][0]))

    # test clearing
    tagm.clear_club_tags(clubs[0][0])
    tagm.clear_club_tags(clubs[1][0])

    print("\nafter clearing:")
    print(tagm.get_club_tags(clubs[0][0]))
    print(tagm.get_club_tags(clubs[1][0]))

    tagm.add_club_tags(clubs[0][0], clubs[0][1])
    tagm.add_club_tags(clubs[1][0], clubs[1][1])

    # test searching
    print("\nsearching tag: game")
    print(tagm.search_club_by_tags(["game"]))
    print("searching tag: buzz")
    print(tagm.search_club_by_tags(["buzz"]))
    print("searching tag: test")
    print(tagm.search_club_by_tags(["test"]))

    # test removal
    print("\nafter removing tags: test")
    tagm.remove_club_tags(clubs[0][0], ["test"])
    tagm.remove_club_tags(clubs[1][0], ["test"])

    print(tagm.get_club_tags(clubs[0][0]))
    print(tagm.get_club_tags(clubs[1][0]))

    del tagm

# uncomment if you want to test
# test_tags()
