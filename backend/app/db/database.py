from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:Stefan@1@127.0.0.1:5432/musicdb", echo=True)