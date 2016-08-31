#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import pprint

from songchecker import model


def main(options):
    print(options)

    query = model.session.query(model.Song)

    if options.artist is not None:
        query = query.filter(model.Artist.name == options.artist)

    results = query.all()

    pp = pprint.PrettyPrinter()
    pp.pprint(results)
