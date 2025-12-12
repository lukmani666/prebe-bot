from sqlalchemy import Column, String, DateTime, func, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Message(Base):
  __tablename__ = "message"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  customer_id = Column(UUID(as_uuid=True), nullable=True, index=True)
  whatsapp_id = Column(String(255), nullable=True, index=True)
  direction = Column(String(16), nullable=False, default="inbound")
  content = Column(Text, nullable=True)
  message_type = Column(String(32), nullable=True)
  sentiment = Column(String(32), nullable=True)
  intent = Column(String(128), nullable=True)
  raw_event = Column(JSON, default={})
  created_at = Column(DateTime(timezone=True), server_default=func.now())