from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models import Artist 
from app.utils.hdf5_files import get_all_files
from app.utils.hdf5_getters import *
from tables import open_file

# Add the artists to the Artist table

data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSongSubset' # 10 000 tracks

def add_artist():

    files = get_all_files(data_folder)
    print(f"Found {len(files)} files to process.\n")

    # Open session
    db: Session = SessionLocal()

    existing_artists = set(db.scalars(select(Artist.artist_name)))

    artists = set()


    for i, path in enumerate(files, 1):
        h5 = None
        try:
            h5 = open_file(path, mode='r')
            artist_name = get_artist_name(h5).decode('utf-8')

            if artist_name not in existing_artists and artist_name not in artists:
                artists.add(artist_name)


        except Exception as e:
            print(f"Error processing {path}: {e}")
        finally:
            if h5 is not None:
                h5.close()

         # Print progress every 1000 files
        if i % 1000 == 0:
            print(f"Processed {i}/{len(files)} files...")

    # Bulk insert
    db.bulk_save_objects([Artist(artist_name=name) for name in artists])

    db.commit()
    db.close()

    print(f"Done: {len(artists)} artists added.")

if __name__ == "__main__":
    add_artist()