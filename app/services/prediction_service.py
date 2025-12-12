from typing import Dict, Any
from joblib import load
import os
import logging
from app.core.config import settings
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(settings.ML_MODELS_PATH, "next_buy_model.pkl")

class PredictionService:
  """
  Loads lightweight ML models and runs predictions. Keep models small for MVP.
  """

  def __init__(self):
    self.db = SessionLocal()
    # lazy load model
    self.model = None
    if os.path.exists(MODEL_PATH):
      try:
        self.model = load(MODEL_PATH)
      except Exception as exc:
        logger.exception("Failed to load ML model: %s", exc)
  
  def extract_features(self, customer_id: str) -> Dict[str, Any]:
    """
    Small feature extraction for MVP: compute recency and frequency placeholders.
    Replace with proper feature store integration.
    """
    # TODO: query orders/messages to compute features
    # Placeholder values:
    features = {
      "recency_days": 30,
      "purchase_frequency": 3,
      "avg_qty": 1.5
    }
    return features
  
  def predict_next_purchase(self, features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a simple prediction structure. If no model available, use heuristic.
    """
    if self.model:
      try:
        X = [list(features.values())]
        days = int(self.model.predict(X)[0])
        return {"days_until_next_purchase": days, "confidence": 0.7}
      except Exception:
        logger.exception("Model inference failed, falling back to heuristic.")
    # heuristic fallback
    days = int(features.get("recency_days", 30) / max(1, features.get("purchase_frequency", 1)))
    return {"days_until_next_purchase": days, "confidence": 0.25}
    
