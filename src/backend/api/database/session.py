# robotsystem/src/backend/api/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.api.core.config import get_settings
from backend.api.database.base import Base

settings = get_settings()

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,  # Use DATABASE_URL aqui, não settings.DATABASE_URL
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """
    Retorna uma sessão SQLAlchemy. Usado como dependência do FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()