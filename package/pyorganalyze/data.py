from collections import defaultdict
import os
import regex
import sqlite3
from orgparse import load


class OrgData:
    tag_hierarchy = defaultdict(set)
    tag_ancestors = defaultdict(set)

    def __init__(self, save_to=':memory:'):
        self.db_path = save_to

        preexisting = os.path.isfile(db_path)
        self.db = sqlite3.connect(db_path)

        # create db if no db exists
        if not preexisting:
            cursor = self.db.cursor()
            with open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'database.sql')) as f:
                cursor.executescript(f.read())

    def __del__(self):
        """Close database connection."""
        global db
        global db_path
        if db:
            db.close()
            db = None
            db_path = None

    def save(self, filename=None):
        """Save in-memory database"""
        if not db:
            raise ValueError("No database connection.")
        if filename and self.db_path == ':memory:':
            # TODO
            raise NotImplementedError
        else:
            self.db.commit()

    def build_tag_ancestors(self, parents=[]):
        """Build tag_ancestors (inefficiently)."""
        it = None
        cur = None
        if parents.len:
            cur = self.tag_hierarchy[parents[-1]]
            it = self.tag_hierarchy[cur]
            self.tag_ancestors[cur].update(parents[:-1])
        else:
            it = self.tag_hierarchy.keys()
        for tag in it:
            self.build_tag_ancestors(
                (parents + [tag]) if parents.len else [cur])

    def process_file(self, filename):
        """Process a parsed org file and save into database."""
        # Scan text before first heading
        # to find tag hierarchies.
        # Tag hierarchies are preserved across all files
        # to keep the program simple
        org_file = load(filename)
        if not self.db:
            raise ValueError('No database connection')
        for line in str(org_file):
            m = regex.match(
                r"^#\+tags:\s+[\[{]\s+([A-Za-z_@]+)\s+:\s+(?:([A-Za-z_@]+)\s+)+[\]}]",
                line,
                regex.I)
            if m:
                parent_tag = m.groups()[0]
                self.tag_hierarchy[parent_tag] = m.captures(2)
        self.build_tag_ancestors()

        # recursively scan for headlines with clocks
        # and save them into database
        cursor = self.db.cursor()
        # TODO
        raise NotImplementedError

    def process_files(self, filenames=[], dirs=[]):
        """Process files and directories (recursively)."""
        if not (filenames or dirs):
            raise ValueError('No input (filename / dirs) specified')
        for d in dirs:
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith(".org"):
                        filenames.append(os.path.join(root, f))

        for filename in filenames:
            self.process_file(filename)
