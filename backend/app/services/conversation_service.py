from typing import Any, Dict
from app.services.whatsapp_service import WhatsAppService
import logging

logger = logging.getLogger(__name__)

class ConversationService:
  """
  Lightweight FSM for conversation decisions. For MVP I use simple rules.
  """
  def __init__(self):
    self.whatsapp = WhatsAppService()

  def handle_message(self, message_record: Any, prediction: Dict[str, Any]) -> None:
    """
    Decide next action and optionally send outbound messages.
    """
    try:
      days = int(prediction.get("days_until_next_purchase", 999))
      customer_phone = None
      # message_record.customer_id might be UUID object; query customer for phone if needed
      # For quick MVP, read from message raw_event
      raw = getattr(message_record, "raw_event", {}) or {}
      customer_phone = raw.get("from") or raw.get("wa_id") or raw.get("phone")

      if days <= 3 and customer_phone:
        text = "Hi, looks like you may be running low on a product you bought earlier. Reply YES to reorder."
        self.whatsapp.send_message(customer_phone, text)
      else:
        logger.debug("No immediate conversational action required for message %s", message_record.id)
    except Exception as exc:
      logger.exception("Error in conversation handling: %s", exc)
