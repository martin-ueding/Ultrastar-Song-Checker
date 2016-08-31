#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import argparse

import songchecker.parser


def main():
    parser = argparse.ArgumentParser(description='Helpers for Ultrastar')
    parser.set_defaults(func=None)
    parser.add_argument('--dbfile', default='ultrastar.sqlite', help='path to SQLite database file')

    subparsers = parser.add_subparsers()

    gendb_parser = subparsers.add_parser('gendb', description='Generate a SQLite database from the song metadata')
    gendb_parser.set_defaults(func=songchecker.parser.main)
    gendb_parser.add_argument('directory', nargs='+', help='directory to scan')
    gendb_parser.add_argument('--verify', action='store_true', help='verify existence of audio and video file', default=False)
    gendb_parser.add_argument('--print-data', action='store_true', help='pretty print read data', default=False)

    options = parser.parse_args()
    if options.func is not None:
        options.func(options)
    else:
        parser.error('A subcommand needs to be given.')


if __name__ == '__main__':
    main()
