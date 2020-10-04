#!/usr/bin/env python3
import os
import sys
import argparse
from organalyze.data import process_file
from orgparse import load


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

    if args.dirs:
        for d in args.dirs:
            if not os.path.isdir(d):
                parser.error(d + ' is not a valid directory')

    if args.files:
        for f in args.files:
            if not os.path.isfile(f):
                parser.error(f + ' is not a valid file name')

    return args



if __name__ == '__main__':
    args = parse_arguments()
    if args.server:
        sys.exit("Web interface is under development")

    org_fnames = args.files
    for d in args.dirs:
        for root, dirs, files in os.walk(d):
            for f in files:
                if f.endswith(".org"):
                    org_fnames.append(os.path.join(root, f))

    for org_fname in org_fnames:
        process_file(load(org_fname))
