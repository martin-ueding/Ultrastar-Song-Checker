#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import songchecker.parser
import songchecker.query
import songchecker.model


def main():
    parser = argparse.ArgumentParser(description='Helpers for Ultrastar')
    parser.set_defaults(func=None)
    parser.add_argument('--dbfile', default='ultrastar.sqlite', help='path to SQLite database file (default: `%(default)s`)')

    subparsers = parser.add_subparsers()

    gendb_parser = subparsers.add_parser('gendb', description='Generate a SQLite database from the song metadata')
    gendb_parser.set_defaults(func=songchecker.parser.main)
    gendb_parser.add_argument('directory', nargs='+', help='directory to scan recursively')
    gendb_parser.add_argument('--verify', action='store_true', help='verify existence of audio and video file', default=False)
    gendb_parser.add_argument('--print-data', action='store_true', help='pretty print read data', default=False)

    query_parser = subparsers.add_parser('query', description='Query the database using various filters.')
    query_parser.set_defaults(func=songchecker.query.main)
    query_parser.add_argument('--paths-only', action='store_true', help='show only the full path (and not a pretty table) for use in e.g. `xargs`')

    query_filter_group = query_parser.add_argument_group('filters', description='Filter the results by various fields. Filters in this group act with a boolean AND. Strings like `title` and `artist` use the `LIKE` comparison, as such you can use the percent sign (`%`) as a wildcard; search for `Awesome Artist%` to find `Awesome Artist and Friend`.')
    query_filter_group.add_argument('--title')
    query_filter_group.add_argument('--artist')
    query_filter_group.add_argument('--genre')
    query_filter_group.add_argument('--has-video', choices=['true', 'false'])

    query_show_group = query_parser.add_argument_group('show columns', description='Flags in this section enable display of more columns in the result table. The order of the columns is fixed in the program, the order of the flags in the invocation has no effect.')

    for field in ['bpm', 'has_video', 'year', 'language', 'genres', 'path']:
        query_show_group.add_argument('--show-{}'.format(field.replace('_', '-')), 
                                  action='store_true')

    query_missing_group = query_parser.add_argument_group('missing fields', description='Flags in this section filter for missing data. Multiple flags are combined using a boolean OR.')

    query_missing_group.add_argument('--missing-genre', action='store_true')
    query_missing_group.add_argument('--missing-year', action='store_true')

    options = parser.parse_args()

    session = init_db(options)

    if options.func is not None:
        options.func(options, session)
    else:
        parser.error('A subcommand needs to be given.')


def init_db(options):
    engine = create_engine('sqlite:///{}'.format(options.dbfile), echo=False)
    songchecker.model.Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session



if __name__ == '__main__':
    main()
