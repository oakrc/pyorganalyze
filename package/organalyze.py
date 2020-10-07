#!/usr/bin/env python3
import argparse
from pyorganalyze.data import OrgData


def parse_arguments():
    """Process command-line arguments."""
    parser = argparse.ArgumentParser(description='Org-agenda Analyzer')
    parser.add_argument('-s', '--server', action='store_true',
                        help="run as web server")
    parser.add_argument('-f', '--files', nargs='+', default=[],
                        help="files to be analyzed")
    parser.add_argument('-d', '--dirs', nargs='+', default=[],
                        help="directories to scan for .org files")
    parser.add_argument('--db', default=':memory:',
                        help="use the specified file as the database "
                        "(creating one if it does not exist)")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_arguments()
    if args.server:
        # TODO web interface
        raise NotImplementedError

    data = OrgData(args.db)
    # if the user is using a preexisting database,
    # then input files are not necessary
    if len(args.files) + len(args.dirs):
        data.process_files(args.files, args.dirs)
