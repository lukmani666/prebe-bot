from sqlalchemy import Column, String, DateTime, Boolean, JSON, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class ChurnFlag(Base):
  __tablename__ = "churn_flags"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
  flagged = Column(Boolean, default=False)
  reason = Column(String(255), nullable=True)
  meta = Column(JSON, default={})
  created_at = Column(DateTime(timezone=True), server_default=func.now())