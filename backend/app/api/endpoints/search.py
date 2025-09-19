from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db.database import engine 

router = APIRouter()

@router.get("/search")
def search_tracks(query: str = Query(..., min_length=1)):
    # Split the strings into words and strip out empties
    words = [word for word in query.strip().split() if word]

    # Update the words and populate the prefixes.
    prefixes = []
    for word in words:
        escaped = word.replace("'", "''") # Replace single quotes
        prefixes.append(f"{escaped}:*")   # Add :* to the words

    # Join the words with & operator for tsquery.
    ts_query = " & ".join(prefixes)

    # Define the SQL statement with parameterised query.
    statement = text("""
        SELECT track.id, track.title, artist.artist_name, genre.genre
        FROM track
        JOIN artist ON artist.id = track.artist_id
        JOIN genre ON genre.id = track.genre_id
        WHERE track.search_vector @@ to_tsquery('english', :q)
        LIMIT 15
    """)

    with engine.connect() as conn:
        results = conn.execute(statement, {"q": ts_query}).fetchall()
        return [{"id": row[0], "title": row[1], "artist_name": row[2], "genre": row[3]} for row in results]