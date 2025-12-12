from pydantic import BaseModel
from typing import Any, Dict, List

class WhatsAppMessage(BaseModel):
  id: str
  from_number: str
  type: str
  body: Dict[str, Any] = {}

class WebhookPayload(BaseModel):
  messages: List[Dict[str, Any]] = []
  statuses: List[Dict[str, Any]] = []