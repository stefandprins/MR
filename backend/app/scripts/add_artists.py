from sqlalchemy.orm import Session
from sqlalchemy import select, text
from app.db.database import SessionLocal
from app.db.models import Artist 
from app.utils.hdf5_files import get_all_files
from app.utils.hdf5_getters import *
from tables import open_file
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import warnings

# Reduce SQLAlchemy logging verbosity
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Suppress HDF5 warnings that cause noise
warnings.filterwarnings('ignore', category=UserWarning, module='tables')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='tables')

# Thread-safe lock for shared data
lock = Lock()

def process_file(file_path):
    """Process a single file and return artist name"""
    h5 = None
    try:
        # More robust file opening with error handling
        h5 = open_file(file_path, mode='r')
        
        # Additional safety check
        if not hasattr(h5.root, 'metadata'):
            return None
            
        artist_name = get_artist_name(h5)
        
        # Handle both string and bytes
        if isinstance(artist_name, bytes):
            artist_name = artist_name.decode('utf-8', errors='ignore')
        
        return artist_name.strip() if artist_name and artist_name.strip() else None
        
    except Exception as e:
        # Silently skip corrupted files
        return None
    finally:
        if h5 is not None:
            try:
                h5.close()
            except:
                pass  # Ignore close errors

def add_artist():
    data_folder = '/mnt/c/Users/dev/Desktop/MRS/MillionSong'
    files = get_all_files(data_folder)
    print(f"Found {len(files)} files to process.\n")

    db: Session = SessionLocal()
    artists = set()
    batch_size = 5000
    total_added = 0
    processed = 0

    # Process files in parallel with reduced workers to avoid segfaults
    with ThreadPoolExecutor(max_workers=2) as executor:  # Reduced from 4 to 2
        # Submit all files to thread pool
        futures = [executor.submit(process_file, file_path) for file_path in files]
        
        # Process results as they complete
        for future in as_completed(futures):
            artist_name = future.result()
            
            if artist_name:
                with lock:  # Thread-safe access to shared data
                    artists.add(artist_name)
                    processed += 1
                    
                    # Bulk insert when batch is full
                    if len(artists) >= batch_size:
                        try:
                            artist_list = list(artists)
                            result = db.execute(
                                text("""
                                    INSERT INTO artist (artist_name) 
                                    SELECT DISTINCT unnest(:names)
                                    ON CONFLICT (artist_name) DO NOTHING
                                """), 
                                {"names": artist_list}
                            )
                            db.commit()
                            added_count = result.rowcount if hasattr(result, 'rowcount') else 0
                            total_added += added_count
                            
                            if added_count > 0:
                                print(f"Inserted {added_count} new artists (Total: {total_added})")
                            
                            artists.clear()
                        except Exception as e:
                            print(f"Bulk insert failed: {e}")
                            db.rollback()
                            artists.clear()
                    
                    # Progress update
                    if processed % 10000 == 0:
                        print(f"Processed {processed:,}/{len(files):,} files... ({processed/len(files)*100:.1f}%)")

    # Insert any remaining artists
    if artists:
        try:
            artist_list = list(artists)
            result = db.execute(
                text("""
                    INSERT INTO artist (artist_name) 
                    SELECT DISTINCT unnest(:names)
                    ON CONFLICT (artist_name) DO NOTHING
                """), 
                {"names": artist_list}
            )
            db.commit()
            added_count = result.rowcount if hasattr(result, 'rowcount') else 0
            total_added += added_count
            
            if added_count > 0:
                print(f"Inserted final {added_count} new artists (Total: {total_added})")
        except Exception as e:
            print(f"Final bulk insert failed: {e}")
            db.rollback()

    db.close()
    print(f"Done: {total_added:,} artists added.")

if __name__ == "__main__":
    add_artist()