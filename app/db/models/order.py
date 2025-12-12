from sqlalchemy import Column, String, DateTime, Numeric, func, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Order(Base):
  __tablename__ = "orders"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
  status = Column(String(32), default="pending")
  total_amount = Column(Numeric(12, 2), nullable=True)
  currency = Column(String(8), default="NGN")
  metadata = Column(JSON, default={})
  created_at = Column(DateTime(timezone=True), server_default=func.now())