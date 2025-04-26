# backend/app/db.py
from sqlmodel import SQLModel, create_engine, Session
from .config import settings

from sqlalchemy.exc import OperationalError

"""
Create the database engine, falling back to local SQLite if connection fails
"""
engine = create_engine(settings.POSTGRES_URL, echo=True)
# Test connection to primary database; fallback to local SQLite if it fails
try:
    conn = engine.connect()
    conn.close()
except Exception:
    fallback_url = "sqlite:///./test.db"
    engine = create_engine(fallback_url, echo=True)

def init_db():
    global engine
    try:
        SQLModel.metadata.create_all(engine)
    except Exception:
        # Fallback to local SQLite file if configured database is unreachable
        fallback_url = "sqlite:///./test.db"
        engine = create_engine(fallback_url, echo=True)
        SQLModel.metadata.create_all(engine)

def get_session():
    # Ensure tables are created before opening a session
    init_db()
    with Session(engine) as session:
        yield session
