from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR

Base = declarative_base()

class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String(400), unique=True, nullable=False)

    tracks = relationship("Track", back_populates="artist")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(100), unique=True, nullable=False)

    tracks = relationship("Track", back_populates="genre")


class Track(Base):
    __tablename__ = "track"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(String(100), unique=True, nullable=False)
    title = Column(String(255), nullable=False)

    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=True)

    duration = Column(Float, nullable=False)
    year = Column(Integer, nullable=True)
    artist_familiarity = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)
    key = Column(Integer, nullable=True)
    mode = Column(Integer, nullable=True)
    time_signature = Column(Integer, nullable=True)

    search_vector = Column(TSVECTOR)

    artist = relationship("Artist", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    segment = relationship("Segment", back_populates="track", uselist=False, cascade="all, delete-orphan")


class Segment(Base):
    __tablename__ = "segment"

    id = Column(Integer, primary_key=True)
    track_id = Column(ForeignKey("track.id"), nullable=False)
    segments = Column(JSONB, nullable=False)
    track = relationship("Track", back_populates="segment")