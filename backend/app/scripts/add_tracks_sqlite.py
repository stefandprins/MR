import sqlite3
import csv
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models import Track, Artist, Genre

# Paths
sqlite_db_path = '/mnt/c/Users/dev/Desktop/MRS/musicdb.sqlite3'
csv_path = '/mnt/c/Users/dev/Desktop/MRS/Backend/genre_mapping.csv'

def load_genre_csv(csv_path):
    genre_mapping = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_genre = row['original_genre'].strip()
                mapped_genre = row['mapped_genre'].strip()
                genre_mapping[original_genre] = mapped_genre
    except Exception as e:
        print(f"Error loading genre mapping: {e}")
    return genre_mapping

def get_genre_id(db: Session, genre_name: str, genre_cache: dict):
    if genre_name not in genre_cache:
        genre = db.query(Genre).filter(Genre.genre == genre_name).first()
        if genre:
            genre_cache[genre_name] = genre.id
        else:
            print(f"Genre not found in database: {genre_name}")
            return None
    return genre_cache.get(genre_name)

def add_tracks_from_sqlite():
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to PostgreSQL
    db: Session = SessionLocal()

    # Load genre mapping
    genre_mapping = load_genre_csv(csv_path)
    print(f"Loaded {len(genre_mapping)} genre mappings")

    # Cache genre and artist data from PostgreSQL
    artist_map = {name: id for id, name in db.query(Artist.id, Artist.artist_name).all()}
    genre_cache = {name: id for id, name in db.query(Genre.id, Genre.genre).all()}
    existing_track_ids = set(db.scalars(select(Track.track_id)))

    # Get tracks joined with artist name and genre
    sqlite_cursor.execute("""
        SELECT 
            t.track_id,
            t.title,
            a.artist_name,
            t.duration,
            t.year,
            t.artist_familiarity,
            t.tempo,
            t.key,
            t.mode,
            t.time_signature,
            g.genre
        FROM track t
        JOIN artist a ON t.artist_id = a.id
        LEFT JOIN genre g ON t.genre_id = g.id
    """)

    rows = sqlite_cursor.fetchall()
    print(f"Found {len(rows)} tracks in SQLite")

    new_tracks = []

    for row in rows:
        (
            track_id, title, artist_name, duration, year, artist_fam,
            tempo, key, mode, time_sig, original_genre
        ) = row

        if track_id in existing_track_ids:
            continue

        # Lookup artist_id in PostgreSQL
        artist_id = artist_map.get(artist_name)
        if not artist_id:
            print(f"Artist not found in PostgreSQL: {artist_name}")
            continue

        # Map and lookup genre_id
        genre_id = None
        if original_genre:
            mapped_genre = genre_mapping.get(original_genre.strip())
            if mapped_genre:
                genre_id = get_genre_id(db, mapped_genre, genre_cache)
            else:
                print(f"Genre mapping not found for: {original_genre}")

        try:
            new_tracks.append(
                Track(
                    track_id=track_id,
                    title=title,
                    artist_id=artist_id,
                    duration=float(duration),
                    year=int(year) if year and year > 0 else None,
                    artist_familiarity=float(artist_fam),
                    tempo=float(tempo),
                    key=int(key),
                    mode=int(mode),
                    time_signature=int(time_sig),
                    genre_id=genre_id
                )
            )
        except Exception as e:
            print(f"Error creating track {track_id}: {e}")

    # Bulk insert to PostgreSQL
    db.bulk_save_objects(new_tracks)
    db.commit()
    db.close()
    sqlite_conn.close()

    print(f"Done: {len(new_tracks)} tracks added from SQLite.")

if __name__ == "__main__":
    add_tracks_from_sqlite()