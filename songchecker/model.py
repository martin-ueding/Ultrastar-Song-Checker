#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

genres_songs_table = Table('genres_songs', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    songs = relationship('Song', back_populates='artist')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Artist(name={})'.format(repr(self.name))


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    bpm = Column(Float, nullable=True)
    has_video = Column(Boolean, nullable=False)
    year = Column(Integer, nullable=True)
    path = Column(String, nullable=False)

    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship('Language', back_populates=__tablename__)

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship('Artist', back_populates=__tablename__)

    genres = relationship('Genre', secondary=genres_songs_table,
                          back_populates='songs')

    def __str__(self):
        return '“{}” by “{}”'.format(self.title, self.artist.name)

    def __repr__(self):
        return 'Song(title={}, artist={}, genres={} bpm={}, has_video={}, year={}, language={}, path={})'.format(
            repr(self.title),
            repr(self.artist),
            repr(self.genres),
            repr(self.bpm),
            repr(self.has_video),
            repr(self.year),
            repr(self.language),
            repr(self.path),
        )


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    songs = relationship('Song', back_populates='language')

    def __str__(self):
        return self.name


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    songs = relationship('Song', secondary=genres_songs_table,
                         back_populates='genres')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Genre(name={})'.format(repr(self.name))


