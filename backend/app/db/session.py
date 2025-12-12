from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

DATABASE_URL = (
  f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
  f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, feature=True, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
  """
  Dependency for FastAPI endpoints that yields a SQLAlchemy session.
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()