from sqlalchemy import Column, String, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Customer(Base):
  __tablename__ = "customers"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  phone = Column(String(32), unique=True, nullable=False, index=True)
  name = Column(String(225), nullable=True)
  email = Column(String(225), nullable=True)
  locale = Column(String(10), nullable=True)
  timezone = Column(String(64), nullable=True)
  meta = Column(JSON, default={})
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  last_seen_at = Column(DateTime(timezone=True), onupdate=func.now())