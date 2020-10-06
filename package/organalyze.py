#!/usr/bin/env python3
import argparse
from pyorganalyze.data import OrgData


def parse_arguments():
    """Process command-line arguments."""
    parser = argparse.ArgumentParser(description='Org-agenda Analyzer')
    parser.add_argument('-s', '--server', action='store_true',
                        help="run as web server")
    parser.add_argument('-f', '--files', nargs='+',
                        help="files to be analyzed")
    parser.add_argument('-d', '--dirs', nargs='+',
                        help="directories to scan for .org files")
    args = parser.parse_args()

    if not (args.files or args.dirs):
        parser.error("No input files specified; use --files or --dirs")

    return args


if __name__ == '__main__':
    args = parse_arguments()
    if args.server:
        # TODO web interface
        raise NotImplementedError

    data = OrgData()
    data.process_files(args.files, args.dirs)
