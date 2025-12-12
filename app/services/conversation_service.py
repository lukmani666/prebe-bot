from typing import Any, Dict
from app.services.whatsapp_service import WhatsAppService
import logging
from app.services.ml_loader import (
  get_dialog_model,
  get_intent_classifier,
  get_sentiment_classifier
)

logger = logging.getLogger(__name__)

class ConversationService:
  """
  Conversation intelligence:
  - Predict intent
  - Predict sentiment
  - Generate contextual replies
  - Trigger reorder automation
  """
  def __init__(self):
    self.whatsapp = WhatsAppService()
  
  #intent classification
  def detect_intent(self, message: str) -> str:
    classifier = get_intent_classifier()
    candidate_labels = [
      "buying intent",
      "complaint",
      "order tracking",
      "refund request",
      "greeting",
      "general inquiry"
    ]
    result = classifier(message, candidate_labels)
    return result["labels"][0]
  
  #Sentiment Analysis
  def detect_sentiment(self, message: str) -> str:
    classifier = get_sentiment_classifier()
    output = classifier(message)[0]
    return output["label"]
  

  #AI Reply Generation
  def generate_ai_reply(self, message: str, history=None) -> str:
    model, tokenizer = get_dialog_model()
    new_input_ids = tokenizer.encode(
      message + tokenizer.eos_token, return_tensors="pt"
    )

    if history is not None:
      input_ids = tokenizer.build_inputs_with_special_tokens(
        history, new_input_ids
      )
    else:
      input_ids = new_input_ids
    
    reply_ids = model.generate(
      input_ids,
      max_length=180,
      pad_token_id=tokenizer.eos_token_id,
      do_sample=True,
      top_p=0.92,
      temperature=0.7
    )

    reply = tokenizer.decode(
      reply_ids[:, input_ids.shape[-1]:][0],
      skip_special_tokens=True
    )
    return reply

  # def handle_message(self, message_record: Any, prediction: Dict[str, Any]) -> None:
  #   """
  #   Decide next action and optionally send outbound messages.
  #   """
  #   try:
  #     days = int(prediction.get("days_until_next_purchase", 999))
  #     customer_phone = None
  #     # message_record.customer_id might be UUID object; query customer for phone if needed
  #     # For quick MVP, read from message raw_event
  #     raw = getattr(message_record, "raw_event", {}) or {}
  #     customer_phone = raw.get("from") or raw.get("wa_id") or raw.get("phone")

  #     if days <= 3 and customer_phone:
  #       text = "Hi, looks like you may be running low on a product you bought earlier. Reply YES to reorder."
  #       self.whatsapp.send_message(customer_phone, text)
  #     else:
  #       logger.debug("No immediate conversational action required for message %s", message_record.id)
  #   except Exception as exc:
  #     logger.exception("Error in conversation handling: %s", exc)

  def handle_message(
    self,
    message_record: Any,
    prediction: Dict[str, Any]
  ) -> None:

    try:
      raw = getattr(message_record, "raw_event", {}) or {}

      customer_phone = (
        raw.get("from") or raw.get("wa_id") or raw.get("phone")
      )
      if not customer_phone:
        logger.warning("No phone number found in inbound message.")
        return

      user_message = raw.get("text") or raw.get("body") or ""
      if not user_message:
        logger.warning("No text found in message.")
        return

      # ML: Detect Intent
      intent = self.detect_intent(user_message)

      # ML: Sentiment
      sentiment = self.detect_sentiment(user_message)

      # Prediction: next buy days
      days = int(prediction.get("days_until_next_purchase", 999))

      # -----------------------------
      # AUTOMATION RULES
      # -----------------------------

      # REORDER LOGIC
      if days <= 3 and intent != "complaint":
          text = (
              "Hi 👋 it looks like you may be running low on something you "
              "purchased earlier.\n\nReply *YES* to reorder instantly."
          )
          self.whatsapp.send_message(customer_phone, text)
          return

      # COMPLAINT HANDLING
      if intent == "complaint":
          reply = (
              "We're sorry to hear that 😔\n"
              "Please share more details about the issue so We can help you quickly."
          )
          self.whatsapp.send_message(customer_phone, reply)
          return

      # REFUND
      if intent == "refund request":
          reply = (
              "We understand you’d like a refund.\n\n"
              "Could you provide your order number so I can process it?"
          )
          self.whatsapp.send_message(customer_phone, reply)
          return

      # ORDER TRACKING
      if intent == "order tracking":
        reply = "Sure! Please share your order ID so I can check the status for you."
        self.whatsapp.send_message(customer_phone, reply)
        return

      # GREETING
      if intent == "greeting":
        reply = "Hi! 👋 How can I help you today?"
        self.whatsapp.send_message(customer_phone, reply)
        return

      # POSITIVE SENTIMENT → Upsell
      if sentiment == "positive" and days < 15:
        text = (
          "Happy to hear that! 😊\n"
          "We also have new arrivals you may like.\nWould you want to see them?"
        )
        self.whatsapp.send_message(customer_phone, text)
        return

      # FALLBACK → AI Reply
      ai_text = self.generate_ai_reply(user_message)
      self.whatsapp.send_message(customer_phone, ai_text)

    except Exception as exc:
        logger.exception("Error in conversation handling: %s", exc)
