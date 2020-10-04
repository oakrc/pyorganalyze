#!/usr/bin/env python3
import argparse
import sqlite3
from orgparse import load

def parse_arguments():
    parser = argparse.ArgumentParser(description='Org-agenda Analyzer')
    return parser.parse_args()

# TODO handle cmd-line arguments
# TODO parse org files
# TODO extract clocks recursively
# TODO put extracted data in in-memory database
# TODO allow saving in-memory database
# TODO querying functionalities
# TODO web interface

if __name__ == '__main__':
    db = sqlite3.connect(':memory:')
