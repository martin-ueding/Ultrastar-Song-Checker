#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import pprint

from songchecker import model


def main(options):
    print(options)

    query = model.session.query(model.Song)

    if options.title is not None:
        print('Filtering title “{}”.'.format(options.title))
        query = query.filter(model.Song.title.like('%{}%'.format(options.title)))

    if options.artist is not None:
        print('Filtering artist “{}”.'.format(options.artist))
        artist_obj = model.session.query(model.Artist).filter(model.Artist.name == options.artist).one()
        query = query.filter(model.Song.artist == artist_obj)

    results = query.all()

    pp = pprint.PrettyPrinter()
    pp.pprint(results)
