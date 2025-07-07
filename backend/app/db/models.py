from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String(255), unique=True, nullable=False)

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

    artist = relationship("Artist", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    segments = relationship("Segment", back_populates="track", cascade="all, delete-orphan")


class Segment(Base):
    __tablename__ = "segment"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("track.id"), nullable=False)
    segment_index = Column(Integer, nullable=False)

    # Timbre features
    timbre_0 = Column(Float)
    timbre_1 = Column(Float)
    timbre_2 = Column(Float)
    timbre_3 = Column(Float)
    timbre_4 = Column(Float)
    timbre_5 = Column(Float)
    timbre_6 = Column(Float)
    timbre_7 = Column(Float)
    timbre_8 = Column(Float)
    timbre_9 = Column(Float)
    timbre_10 = Column(Float)
    timbre_11 = Column(Float)

    # Pitch features
    pitch_0 = Column(Float)
    pitch_1 = Column(Float)
    pitch_2 = Column(Float)
    pitch_3 = Column(Float)
    pitch_4 = Column(Float)
    pitch_5 = Column(Float)
    pitch_6 = Column(Float)
    pitch_7 = Column(Float)
    pitch_8 = Column(Float)
    pitch_9 = Column(Float)
    pitch_10 = Column(Float)
    pitch_11 = Column(Float)

    loudness_max = Column(Float)
    confidence = Column(Float)

    track = relationship("Track", back_populates="segments")