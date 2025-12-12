from sqlalchemy.orm import Session
from app.db.models.message import Message
from typing import List
import uuid

class MessageRepository:
  def __init__(self, db: Session):
    self.db = db
  
  def create(self, data: dict) -> Message:
    msg = Message(
      id=uuid.uuid4(),
      customer_id=data.get("customer_id"),
      whatsapp_id=data.get("whatsapp_id"),
      direction=data.get("direction", "inbound"),
      content=data.get("content"),
      message_type=data.get("message_type"),
      raw_event=data.get("raw_event") or {},
    )
    self.db.add(msg)
    self.db.commit()
    self.db.refresh(msg)
    return msg
  
  def list_for_customer(self, customer_id, limit=100):
    return (
      self.db.query(Message)
      .filter(Message.customer_id == customer_id)
      .order_by(Message.created_at.desc())
      .limit(limit)
      .all()
    )