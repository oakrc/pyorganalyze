from collections import defaultdict
import os
import regex
import sqlite3

tag_hierarchy = defaultdict(set)
tag_ancestors = defaultdict(set)


def create_db(path=':memory:'):
    """Create a database connection."""
    global db
    global db_path
    db_path = path
    preexisting = os.path.isfile(db_path)
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    if not preexisting:
        with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'database.sql')) as f:
            cursor.executescript(f.read())


def save_db(filename):
    """Save in-memory database"""
    if db_path != ':memory:' and db:
        pass


def close_db():
    """Close database connection."""
    global db
    global db_path
    if db:
        db.close()
        db = None
        db_path = None


def build_tag_ancestors(parents=[]):
    """Build tag_ancestors (inefficiently)."""
    it = None
    cur = None
    if parents.len:
        cur = tag_hierarchy[parents[-1]]
        it = tag_hierarchy[cur]
        tag_ancestors[cur].update(parents[:-1])
    else:
        it = tag_hierarchy.keys()
    for tag in it:
        build_tag_ancestors((parents + [tag]) if parents.len else [cur])


def process_file(org_file):
    """Process a parsed org file and save into database."""
    # TODO tags tree; see tag_{hierarchy,parents}
    # scan text before first heading
    for line in str(org_file):
        m = regex.match(
            r"^#\+tags:\s+[\[{]\s+([A-Za-z_@]+)\s+:\s+(?:([A-Za-z_@]+)\s+)+[\]}]",
            line,
            regex.I)
        if m:
            parent_tag = m.groups()[0]
            tag_hierarchy[parent_tag] = m.captures(2)
    build_tag_ancestors()
