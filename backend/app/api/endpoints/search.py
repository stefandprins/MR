from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db.database import engine  # Assuming engine is defined here

router = APIRouter()

@router.get("/search")
# def search_tracks(q: str = Query(..., min_length=1)):
#     with engine.connect() as conn:
#         stmt = text("""
#                         SELECT id, title, artist_name
#                         FROM api_song
#                         WHERE LOWER(title) LIKE LOWER(:q)
#                         OR LOWER(artist_name) LIKE LOWER(:q)
#                         LIMIT 15
#                     """)
#         results = conn.execute(stmt, {"q": f"%{q}%"}).fetchall()
#         return [{"id": row[0], "title": row[1], "artist_name": row[2]} for row in results]
    
# def search_tracks(query):
#     words = query.lower().split()
#     conditions = " AND ".join(
#         [f"(LOWER(title) LIKE :w{i} OR LOWER(artist_name) LIKE :w{i})" for i in range(len(words))]
#     )
#     stmt = text(f"""
#         SELECT id, title, artist_name
#         FROM api_song
#         WHERE {conditions}
#         LIMIT 15
#     """)
#     params = {f"w{i}": f"%{word}%" for i, word in enumerate(words)}
    
#     with engine.connect() as conn:
#         results = conn.execute(stmt, params).fetchall()
#         return [{"id": row[0], "title": row[1], "artist_name": row[2]} for row in results]

def search_tracks(query):
    # Prepare the FTS5 query string (space-separated tokens)
    fts_query = query.replace('"', '""')  # escape quotes

    stmt = text("""
        SELECT s.id, s.title, s.artist_name
        FROM api_song s
        JOIN api_song_fts ON s.rowid = api_song_fts.rowid
        WHERE api_song_fts MATCH :q
        LIMIT 15
    """)
    
    with engine.connect() as conn:
        results = conn.execute(stmt, {"q": fts_query}).fetchall()
        return [{"id": row[0], "title": row[1], "artist_name": row[2]} for row in results]