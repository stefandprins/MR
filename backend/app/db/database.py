from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///app/db/db.sqlite3", echo=True)

# def search_tracks(query):
#     with engine.connect() as conn:
#         stmt = text("SELECT * FROM api_song WHERE title LIKE :q")
#         results = conn.execute(stmt, {"q": f"%{query}%"}).fetchall()
#         return [{"id": row[0], "title": row[1]} for row in results]