from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator
from urllib.parse import quote_plus

PASSWORD = quote_plus(settings.POSTGRES_PASSWORD)

DATABASE_URL = (
  f"postgresql://{settings.POSTGRES_USER}:{PASSWORD}"
  f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
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