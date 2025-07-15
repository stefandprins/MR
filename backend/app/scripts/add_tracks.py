import csv
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models import Track, Artist, Genre
from app.utils.hdf5_files import get_all_files
from app.utils.hdf5_getters import *
from tables import open_file

# Add the tracks to the Track table

# data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSongSubset'
data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSong'
csv_path = '/mnt/c/Users/dev/Desktop/MRS/Backend/genre_mapping.csv'

def load_genre_csv(csv_path):
    # Load genre mapping from CSV file
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
    # Get genre ID from cache or database
    if genre_name not in genre_cache:
        genre = db.query(Genre).filter(Genre.genre == genre_name).first()
        if genre:
            genre_cache[genre_name] = genre.id
        else:
            print(f"Genre not found in database: {genre_name}")
            return None
    return genre_cache.get(genre_name)

def map_track_genre(track_genres, genre_mapping):
    if track_genres is None or len(track_genres) == 0:
        return None

    # Convert to list if it's a NumPy array
    if hasattr(track_genres, 'tolist'):
        track_genres = track_genres.tolist()

    # Decode bytes if needed
    first_genre = track_genres[0]
    if isinstance(first_genre, bytes):
        first_genre = first_genre.decode('utf-8')
    
    first_genre = first_genre.strip()
    mapped_genre = genre_mapping.get(first_genre)

    if not mapped_genre:
        print(f"Genre mapping not found for: {first_genre}")
        return None
    
    return mapped_genre

def add_tracks():
    files = get_all_files(data_folder)
    db: Session = SessionLocal()

    # Load genre mapping
    genre_mapping = load_genre_csv(csv_path)
    print(f"Loaded {len(genre_mapping)} genre mappings")

    # Cache existing artist names and IDs
    artist_map = {name: id for id, name in db.query(Artist.id, Artist.artist_name).all()}
    existing_track_ids = set(db.scalars(select(Track.track_id)))

    # Cache genre names and IDs
    genre_cache = {name: id for id, name in db.query(Genre.id, Genre.genre).all()}
    print(f"Loaded {len(genre_cache)} genres from database")

    new_tracks = []

    for i, path in enumerate(files, 1):
        h5 = None
        try:
            h5 = open_file(path, mode='r')
            track_id = get_track_id(h5).decode('utf-8')

            if track_id in existing_track_ids:
                continue

            artist_name = get_artist_name(h5).decode('utf-8')
            title = get_title(h5).decode('utf-8')
            duration = get_duration(h5)
            year = get_year(h5)
            artist_fam = get_artist_familiarity(h5)
            tempo = get_tempo(h5)
            key = get_key(h5)
            mode = get_mode(h5)
            time_sig = get_time_signature(h5)

            # Get artist ID
            artist_id = artist_map.get(artist_name)
            if not artist_id:
                print(f"Artist not found for track {track_id}: {artist_name}")
                continue

            # Get and map genre
            genre_id = None
            try:
                track_genres = get_artist_terms(h5, songidx=0)
                mapped_genre = map_track_genre(track_genres, genre_mapping)
                if mapped_genre:
                    genre_id = get_genre_id(db, mapped_genre, genre_cache)
            except Exception as e:
                print(f"Error processing genre for track {track_id}: {e}")

            new_tracks.append(
                Track(
                    track_id=track_id,
                    title=title,
                    artist_id=artist_id,
                    duration=float(duration),
                    year=int(year) if year > 0 else None,
                    artist_familiarity=float(artist_fam),
                    tempo=float(tempo),
                    key=int(key),
                    mode=int(mode),
                    time_signature=int(time_sig),
                    genre_id=genre_id
                )
            )

        except Exception as e:
            print(f"Error reading {path}: {e}")
        finally:
            if h5:
                h5.close()

        # Print progress every 1000 files
        if i % 1000 == 0:
            print(f"Processed {i}/{len(files)} files...")

    # Bulk insert
    db.bulk_save_objects(new_tracks)
    db.commit()
    db.close()

    print(f"Done: {len(new_tracks)} tracks added.")

if __name__ == "__main__":
    add_tracks()