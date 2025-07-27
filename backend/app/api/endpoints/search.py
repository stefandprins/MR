from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db.database import engine 

router = APIRouter()

@router.get("/search")
def search_tracks(query: str = Query(..., min_length=1)):
    # 1) Split into words and strip out empties
    words = [w for w in query.strip().split() if w]

    # 2) Escape quotes and add :* for each term
    prefixes = []
    for w in words:
        escaped = w.replace("'", "''")   # 
        prefixes.append(f"{escaped}:*")  # 

    # 3) Join with AND operator for tsquery
    ts_query = " & ".join(prefixes)

    stmt = text("""
        SELECT track.id, track.title, artist.artist_name, genre.genre
        FROM track
        JOIN artist ON artist.id = track.artist_id
        JOIN genre ON genre.id = track.genre_id
        WHERE track.search_vector @@ to_tsquery('english', :q)
        LIMIT 15
    """)

    with engine.connect() as conn:
        results = conn.execute(stmt, {"q": ts_query}).fetchall()
        return [{"id": row[0], "title": row[1], "artist_name": row[2], "genre": row[3]} for row in results]