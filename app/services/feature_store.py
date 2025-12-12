from typing import Dict
from app.db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)

class FeatureStore:
  """
  Minimal feature store for MVP. Reads from Postgres for batch features and uses Redis for caching.
  """

  def __init__(self):
    self.db = SessionLocal()
    # Optionally integrate Redis here

  def get_customer_features(self, customer_id: str) -> Dict:
    """
    Compute or retrieve features for a customer.
    """
    # TODO: implement actual aggregations (orders/messages)
    features = {
      "recency_days": 30,
      "purchase_frequency": 3,
      "avg_qty": 1
    }

    return features