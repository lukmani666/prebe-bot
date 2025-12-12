from sqlalchemy import Column, String, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Conversation(Base):
  __tablename__ = "conversation"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
  state = Column(String(64), default="idle")
  meta = Column(JSON, default={})
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

