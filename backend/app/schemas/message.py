from pydantic import BaseModel
from typing import Optional, Any, Dict
from uuid import UUID

class MessageCreate(BaseModel):
  customer_id: Optional[UUID]
  whatsapp_id: Optional[str]
  content: Optional[str]
  message_type: Optional[str] = "text"
  raw_event: Optional[Dict[str, Any]] = {}


class MessageRead(MessageCreate):
  id: UUID
  created_at: Optional[str] = None

  model_config = {
    "from_attributes": True
  }