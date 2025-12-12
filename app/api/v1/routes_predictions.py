from fastapi import APIRouter, Depends, HTTPException
from app.services.prediction_service import PredictionService
from app.schemas.prediction import NextPurchaseResponse
from app.db.session import get_db

router = APIRouter()

@router.get("/{customer_id}", response_model=NextPurchaseResponse)
def get_next_purchase(customer_id: str):
  svc = PredictionService()
  features = svc.extract_features(customer_id)
  pred = svc.predict_next_purchase(features)
  return NextPurchaseResponse(**pred)

@router.post("/intent")
def predict_intent(payload: dict):
    from app.services.conversation_service import ConversationService
    svc = ConversationService()
    intent = svc.detect_intent(payload["text"])
    return {"intent": intent}
