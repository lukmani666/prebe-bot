from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from app.services.whatsapp_service import WhatsAppService
from app.services.conversation_service import ConversationService
from app.services.prediction_service import PredictionService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
  """
  Entrypoint for incoming WhatsApp webhooks.
  Accepts JSON payloads as delivered by WhatsApp Cloud API.
  """
  payload = await request.json()
  # Basic validation: adapt to actual WhatsApp payload structure
  messages = payload.get("messages") or []
  if not messages:
    # Some WhatsApp webhooks might contain statuses only; handle them later
    logger.info("Webhook received with no messages: %s", payload)
    return {"status": "no_message"}
  
  for msg in messages:
    # process in background to keep webhook response fast
    background_tasks.add_task(process_message, msg)
  
  return {"status": "accepted"}

def process_message(msg: dict):
  """
  Background sync handler to process a single message event.
  """
  try:
    whatsapp = WhatsAppService()
    conv = ConversationService()
    pred = PredictionService()

    message_record = whatsapp.save_message(msg)
    features = pred.extract_features(str(message_record.customer_id))
    predicttion = pred.predict_next_purchase(features)
    conv.handle_message(message_record, predicttion)
  except Exception as exc:
    logger.exception("Error processing message: %s", exc)