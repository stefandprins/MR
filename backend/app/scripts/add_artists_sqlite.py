
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.database import SessionLocal  # Your existing PostgreSQL session

def copy_artists_from_sqlite():
    # Connect to SQLite database
    sqlite_db_path = '/mnt/c/Users/dev/Desktop/MRS/musicdb.sqlite3'  # Update this path
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Get all artist names from SQLite
    sqlite_cursor.execute("SELECT DISTINCT artist_name FROM artist WHERE artist_name IS NOT NULL AND artist_name != ''")
    artist_names = [row[0] for row in sqlite_cursor.fetchall()]
    
    print(f"Found {len(artist_names)} artists in SQLite database")
    
    # Connect to PostgreSQL
    pg_db = SessionLocal()
    
    # Insert artists in batches
    batch_size = 5000
    total_added = 0
    
    for i in range(0, len(artist_names), batch_size):
        batch = artist_names[i:i + batch_size]
        
        try:
            # Use INSERT ON CONFLICT to handle duplicates
            result = pg_db.execute(
                text("""
                    INSERT INTO artist (artist_name) 
                    SELECT DISTINCT unnest(:names)
                    ON CONFLICT (artist_name) DO NOTHING
                """), 
                {"names": batch}
            )
            
            pg_db.commit()
            added_count = result.rowcount if hasattr(result, 'rowcount') else 0
            total_added += added_count
            
            print(f"Processed {i + len(batch):,}/{len(artist_names):,} artists, added {added_count} new ones")
            
        except Exception as e:
            print(f"Error inserting batch: {e}")
            pg_db.rollback()
    
    # Cleanup
    sqlite_conn.close()
    pg_db.close()
    
    print(f"Done! Added {total_added:,} new artists to PostgreSQL")

if __name__ == "__main__":
    copy_artists_from_sqlite()