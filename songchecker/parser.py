#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import os
import pprint
import re
import shlex
import sys

import chardet

from songchecker import model


PATTERN = re.compile(r'^#([^:]+):(.*)$')


def meta_file_to_dict(filename):
    data = {}

    with open(filename, 'rb') as f:
        bytes_ = f.read()
        detected = chardet.detect(bytes_)

    with open(filename, encoding=detected['encoding']) as f:
        for line in f:
            match = PATTERN.match(line)
            if match:
                key = match.group(1)
                value = match.group(2)
                data[key] = value

    return data


def referred_exists(dirname, filename):
    return os.path.isfile(os.path.join(dirname, filename))


def main(options):
    pp = pprint.PrettyPrinter()

    # List for broken files.
    broken_files = []

    # Iterate through all the directories given on the command line.
    for directory in options.directory:
        # Recursively walk through the directory tree.
        for dirname, dirs, files in os.walk(directory):
            # Iterate through the files in the directory.
            for file in files:
                # First create the full path of the current file.
                path = os.path.join(dirname, file)

                # If it is not a text file, ignore this file.
                if not file.endswith('.txt'):
                    continue

                # Get the meta data.
                data = meta_file_to_dict(path)

                # Print meta data if desired.
                if options.print_data:
                    print(path)
                    pp.pprint(data)
                    print()

                # Define a helper function that checks whether the key exists
                # and the associated file exists in the same directory.
                def check_for(key):
                    if key in data:
                        exists = referred_exists(dirname, data[key])
                        return exists
                    else:
                        return False

                # If files should be verified, check all the following keys.
                if options.verify:
                    keys = ['MP3', 'VIDEO']
                    for key in keys:
                        if not check_for(key):
                            broken_files.append((path, key))

                # We are about to create a new song for the database. In this
                # dictionary we collect all the data that is going to be
                # inserted into the database table. 
                for_db = {
                        'title': data['TITLE'],
                        'has_video': check_for('VIDEO'),
                        }

                # If the artist is known in the database, we want to use that
                # one. For this we query all the artists that have the same
                # name as the current song has in its file.
                artists_obj = model.session.query(model.Artist).filter(model.Artist.name == data['ARTIST']).all()

                # If there is no artist in the database, create a new one and
                # assign it to our song.
                if len(artists_obj) == 0:
                    artist_obj = model.Artist(name=data['ARTIST'])
                    model.session.add(artist_obj)
                    for_db['artist'] = artist_obj
                # If there is one or more artists with the same name, use the
                # first one. Ideally, there should never occur since the `name`
                # in the `artists` table is marked as unique.
                else:
                    for_db['artist'] = artists_obj[0]


                if 'GENRE' in data:
                    genres = data['GENRE'].split(',')
                    for_db['genres'] = []

                    for genre in genres:
                        genres_obj = model.session.query(model.Genre).filter(model.Genre.name == genre).all()
                        if len(genres_obj) == 0:
                            genre_obj = model.Genre(name=genre)
                            model.session.add(genre_obj)
                            for_db['genres'].append(genre_obj)
                        else:
                            for_db['genres'].append(genre_obj[0])

                # Create a new song object with the fields worked out above.
                # Then add it to the database and end the transaction.
                pp.pprint(for_db)
                song_obj = model.Song(**for_db)
                model.session.add(song_obj)
                model.session.commit()

    # Print a list with all broken files to `stderr`.
    for path, message in broken_files:
        print(shlex.quote(path), message, file=sys.stderr)


if __name__ == '__main__':
    main()
