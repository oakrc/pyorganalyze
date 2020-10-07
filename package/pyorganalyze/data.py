from collections import defaultdict
import os
import regex
import sqlite3
from orgparse import load
from datetime import timedelta, datetime, time


class OrgData:
    def __init__(self, save_to=':memory:'):
        self.db_path = save_to
        self.tag_hierarchy = defaultdict(set)
        self.tag_ancestors = defaultdict(set)

        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()
        with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'database.sql')) as f:
            self.exec(f.read())

    def __del__(self):
        """Close database connection"""
        if self.db:
            self.db.close()

    def query(self, sql: str, args=[]):
        """Run a single SQL query"""
        return self.cursor.execute(sql, args)

    def exec(self, sql: str):
        """Execute SQL script"""
        return self.cursor.executescript(sql)

    def save(self, filename=None):
        """Save in-memory database"""
        if filename and self.db_path == ':memory:':
            saved = sqlite3.connect(filename)
            self.db_path = filename
            with saved:
                self.db.backup(saved)
            self.db.close()
            self.db = saved
        self.db.commit()

    def __build_tag_ancestors(self, parents=[]):
        """Build tag_ancestors (inefficiently)"""
        # assuming there are no loops
        if len(parents):
            cur = parents[-1]
            it = self.tag_hierarchy[cur]
            self.tag_ancestors[cur].update(parents[:-1])
        else:
            it = self.tag_hierarchy.copy().keys()
        for tag in it:
            self.__build_tag_ancestors(parents + [tag])

    def __make_hierarchichal(self, tags: set) -> set:
        """Inherit tags from tag_hierarchy"""
        new_tags = set()
        for tag in tags:
            new_tags.update(self.tag_ancestors[tag])
        return new_tags

    def __walk_org_node(self, filename, node, parents=[]):
        """Recursively save headlines with clocks into db"""
        if len(node.clock):
            prop = node.properties.get
            is_archived = prop('ARCHIVE_TIME') is not None
            headline = [filename + ' ➤ ' + prop('ARCHIVE_FILE')
                        if is_archived else filename,
                        prop('ARCHIVE_OLPATH').replace('/', ' ➤ ')
                        if is_archived else ' ➤ '.join(parents),
                        node.todo,
                        node.heading,
                        prop('ARCHIVE_CATEGORY')
                        if is_archived else prop('CATEGORY')
                        ]
            self.query("INSERT INTO headlines "
                       "(filename,parent,todo,heading,category)"
                       " VALUES (?,?,?,?,?)", headline)

            headline_id = self.cursor.lastrowid

            tags = node.tags | set((prop('ARCHIVE_ITAGS') or '').split(' '))
            self.__make_hierarchichal(tags)
            # save tags
            for tag in tags:
                self.query("INSERT INTO headline_tags VALUES (?,?)",
                           [headline_id, tag])

            # save clocks
            for clock in node.clock:
                clocks = []
                # split the clock into multiple single-day ones
                if clock.start.date() != clock.end.date():
                    clocks.append([headline_id, clock.start,
                                   datetime.combine(clock.start.date(),
                                                    time.max)])
                    second = datetime.combine(clock.start.date()
                                              + timedelta(days=1),
                                              time.min)
                    start = datetime.combine(second, time.min)
                    end = datetime.combine(second, time.max)
                    while end < clock.end:
                        clocks.append([headline_id, start, end])
                        start += timedelta(days=1)
                        end += timedelta(days=1)
                    clocks.append([headline_id, start, clock.end])
                else:
                    clocks.append([headline_id, clock.start, clock.end])
                for c in clocks:
                    self.query("INSERT INTO clocks VALUES (?,?,?)", c)

        for child in node.children:
            parents.append(node.heading)
            self.__walk_org_node(filename, child, parents)

    def process_file(self, filename: str):
        """Process an org file and save into database"""
        # Scan text before first heading to find tag hierarchies.
        # Tag hierarchies are preserved across all files to keep
        # the program simple.
        org_file = load(filename)
        for line in str(org_file).split('\n'):
            e = r"^#\+tags:\s+[\[{]\s+([a-z_@]+)\s+:\s+(?:([a-z_@]+)\s+)+[\]}]"
            m = regex.match(e, line, regex.I)
            if m:
                parent_tag = m.groups()[0]
                self.tag_hierarchy[parent_tag] = m.captures(2)
        self.__build_tag_ancestors()

        for node in org_file.children:
            self.__walk_org_node(filename, node)

        self.save()

    def process_files(self, filenames=[], dirs=[]):
        """Process files and directories (recursively)"""
        filenames = filenames or []
        dirs = dirs or []
        if len(filenames) + len(dirs) == 0:
            raise ValueError('No input (filename / dirs) specified')
        for d in dirs:
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith(".org"):
                        filenames.append(os.path.join(root, f))

        for filename in filenames:
            self.process_file(filename)
