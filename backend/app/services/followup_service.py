from typing import Dict
from app.services.whatsapp_service import WhatsAppService
import logging

logger = logging.getLogger(__name__)

class FollowupService:
  """
  Responsible for scheduling and sending follow-up messages.
  In MVP, followups can be enqueued into Celery for execution.
  """
  def __init__(self):
    self.whatsapp = WhatsAppService()
  
  def send_followup(self, phone: str, payload: Dict):
    """
    Send followup message immediately (or call Celery task).
    """
    text = payload.get("text", "Reminder from PreBe")
    # For production, call Celery delay method here
    return self.whatsapp.send_message(phone, text)
