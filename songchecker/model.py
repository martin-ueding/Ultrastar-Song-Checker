#!/usr/bin/python3
# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///songs.sqlite', echo=True)

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    songs = relationship('Song', back_populates='artist')


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    bpm = Column(Integer, nullable=True)
    has_video = Column(Boolean, nullable=False)
    year = Column(Integer, nullable=True)

    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship('Language', back_populates=__tablename__)

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship('Artist', back_populates=__tablename__)

    #genre = Column


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    songs = relationship('Song', back_populates='language')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
