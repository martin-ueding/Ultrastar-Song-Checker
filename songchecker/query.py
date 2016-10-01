#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import shlex
import sys
import pprint

import prettytable
import sqlalchemy.orm
from sqlalchemy import or_

from songchecker import model


def main(options, session):
    query = session.query(model.Song)

    try:
        if options.title is not None:
            print('Filtering title “{}”.'.format(options.title))
            query = query.filter(model.Song.title.like(options.title))

        if options.artist is not None:
            print('Filtering artist “{}”.'.format(options.artist))
            artist_obj = session.query(model.Artist).filter(model.Artist.name.like(options.artist)).first()
            query = query.filter(model.Song.artist == artist_obj)

        if options.has_video is not None:
            print('Filtering has_video “{}”.'.format(options.has_video))
            has_video = True if options.has_video == 'true' else False
            query = query.filter(model.Song.has_video == has_video)

        if options.genre is not None:
            print('Filtering genre “{}”.'.format(options.genre))
            genre_obj = session.query(model.Genre).filter(model.Genre.name == options.genre).one()
            query = query.outerjoin(model.Song.genres).filter(model.Song.genres.contains(genre_obj))

        if options.language is not None:
            print('Filtering language “{}”.'.format(options.language))
            language_objs = session.query(model.Language).filter(model.Language.name.like(options.language)).all()
            lang_filters = [
                model.Song.language == language_obj
                for language_obj in language_objs
            ]
            query = query.filter(or_(*lang_filters))

    except sqlalchemy.orm.exc.NoResultFound:
        print('Could not find the related object, no results')
        sys.exit(1)

    results = query.all()

    if options.missing_genre or options.missing_year or options.missing_language:
        results = [song
                   for song in results
                   if (options.missing_genre and len(song.genres) == 0)
                   or (options.missing_year and song.year is None)
                   or (options.missing_language and song.language is None)
                  ]

    if len(results) == 0:
        print()
        print('No results.')
    elif options.paths_only:
        for element in results:
            print(shlex.quote(element.path))
    else:
        print()
        format_table(results, options)


def format_table(elements, options):
    columns = ['Title', 'Artist', 'Genres']

    if options.show_bpm:
        columns.append('BPM')
    if options.show_has_video:
        columns.append('Video')
    if options.show_year:
        columns.append('Year')
    if options.show_language:
        columns.append('Language')
    if options.show_path:
        columns.append('Path')

    table = prettytable.PrettyTable(columns)
    table.align = 'l'

    for element in elements:
        row = [
            str(element.title),
            str(element.artist),
            ', '.join(map(str, element.genres)),
        ]

        if options.show_bpm:
            row.append(str(element.bpm))
        if options.show_has_video:
            row.append(str(element.has_video))
        if options.show_year:
            row.append(str(element.year))
        if options.show_language:
            row.append(str(element.language))
        if options.show_path:
            row.append(shlex.quote(element.path))

        table.add_row(row)
    print(table)
