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