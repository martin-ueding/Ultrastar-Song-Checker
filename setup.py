#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

setup(
    author="Martin Ueding",
    author_email="dev@martin-ueding.de",
    description="Meta data helper for Ultrastar karaoke software",
    license="GPL2",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",

    ],
    name="songchecker",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'songchecker = songchecker.__main__:main',
        ],
    },
    install_requires=[
        'prettytable',
        'sqlalchemy',
    ],
    url="https://github.com/martin-ueding/Ultrastar-Song-Checker",
    version="0.1",
)
