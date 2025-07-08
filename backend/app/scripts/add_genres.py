from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Genre 

# Add the genres to the Genre table

def add_genres():
    # List of genres to add.
    genres = [
        "Pop", "Electronic", "Rock", "Folk", "Metal",
        "Jazz", "Hip-Hop", "Blues", "Country", "Reggae",
        "R&B", "Classical"
    ]

    created = 0
    skipped = 0

    # Open session
    db: Session = SessionLocal()

    # Loop through the list of genres. Add the genre to the table if it is not found.
    try:
        for genre in genres:
            existing = db.query(Genre).filter(Genre.genre == genre).first() # Check the table for genre.

            # Add the genre if it doesn't exist or skip.
            if not existing:
                new_genre = Genre(genre=genre)
                db.add(new_genre)
                created += 1
            else:
                skipped += 1

        db.commit()
        print(f"Load Complete: {created} added, {skipped} skipped.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    add_genres()