from sqlalchemy import Column, String, DateTime, JSON, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Prediction(Base):
  __tablename__ = "predictions"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
  model_name = Column(String(128), nullable=False)
  model_version = Column(String(64), nullable=True)
  Prediction = Column(JSON, nullable=True)
  score = Column(Numeric, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())