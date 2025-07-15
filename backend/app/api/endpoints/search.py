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
        escaped = w.replace("'", "''")   # double up single quotes
        prefixes.append(f"{escaped}:*")  # now safe—no backslashes in here

    # 3) Join with AND operator for tsquery
    ts_query = " & ".join(prefixes)

    stmt = text("""
        SELECT track.id, track.title, artist.artist_name AS artist_name
        FROM track
        JOIN artist ON track.artist_id = artist.id
        WHERE track.search_vector @@ to_tsquery('english', :q)
        LIMIT 15
    """)

    with engine.connect() as conn:
        results = conn.execute(stmt, {"q": ts_query}).fetchall()
        return [{"id": row[0], "title": row[1], "artist_name": row[2]} for row in results]