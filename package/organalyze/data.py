import sqlite3

db = sqlite3.connect(':memory:')
cursor = db.cursor()
with open('database.sql') as f:
    cursor.executescript(f.read())

# TODO tags tree
tag_hierarchy = {}
tag_parent_lookup = {}


def process_file(org_file):
    pass
