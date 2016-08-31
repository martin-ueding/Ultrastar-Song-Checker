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

    broken_files = []

    for directory in options.directory:
        for dirname, dirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(dirname, file)
                if not file.endswith('.txt'):
                    continue

                data = meta_file_to_dict(path)
                if options.print_data:
                    print(path)
                    pp.pprint(data)
                    print()

                def check_for(key):
                    if key in data:
                        exists = referred_exists(dirname, data[key])
                        if exists:
                            return True
                        else:
                            broken_files.append((path, key))
                            return False
                    else:
                        return False

                if options.verify:
                    keys = ['MP3', 'VIDEO']
                    [check_for(key) for key in keys]

                for_db = {
                        'title': data['TITLE'],
                        'has_video': check_for('VIDEO'),
                        }

                song = model.Song(**for_db)

                model.session.add(song)
    model.session.commit()

    for path, message in broken_files:
        print(shlex.quote(path), message, file=sys.stderr)


if __name__ == '__main__':
    main()
