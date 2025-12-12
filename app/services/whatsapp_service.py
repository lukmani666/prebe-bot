from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.repositories.message_repo import MessageRepository
from app.db.repositories.customer_repo import CustomerRepository
from app.db.models.message import Message
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
  """
  Responsible for persisting inbound messages and sending outbound messages.
  Real WhatsApp Cloud API integration should be added where noted.
  """

  def __init__(self):
    self.db = SessionLocal()
    self.msg_repo = MessageRepository(self.db)
    self.cust_repo = CustomerRepository(self.db)

  def save_message(self, raw_msg: dict) -> Message:
    """
    Extract minimal fields from incoming webhook and save.
    raw_msg is expected to be the WhatsApp message object.
    """
    # extract phone / text fields depending on payload shape
    phone = None
    content = None
    whatsapp_id = raw_msg.get("id") or raw_msg.get("wa_id")

    # Typical payloads vary; adapt as needed
    if "from" in raw_msg:
      phone = raw_msg.get("from")
    if "text" in raw_msg and isinstance(raw_msg.get("text"), dict):
      content = raw_msg["text"].get("body")
    elif "body" in raw_msg:
      content = raw_msg.get("body")
    else:
      content = str(raw_msg)
    
    # ensure customer exists
    customer =None
    if phone:
      customer = self.cust_repo.get_by_phone(phone)
      if not customer:
        # create minimal profile
        from app.schemas.customer import CustomerCreate
        customer = self.cust_repo.create(
          CustomerCreate(phone=phone, name=None, email=None, locale=None, timezone=None, meta={})
        )
    
    message_data = {
      "customer_id": getattr(customer, "id", None),
      "whatsapp_id": whatsapp_id,
      "direction": "inbound",
      "content": content,
      "message_type": raw_msg.get("type", "text"),
      "raw_event": raw_msg,
    }

    return self.msg_repo.create(message_data)
  
  def send_message(self, phone: str, text: str) -> Dict:
    """
    Send outbound message to a phone number using WhatsApp Cloud API.
    For MVP this is a stub that logs message. Implement HTTP call + templates in production.
    """
    # TODO: implement WhatsApp Cloud API call using settings.WHATSAPP_TOKEN
    logger.info("send_message stub to %s: %s", phone, text)
    return {"status": "queued", "phone": phone, "text": text}