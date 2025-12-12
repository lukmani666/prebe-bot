from typing import Dict

def compute_basic_features(order_history: list) -> Dict:
  """
  Minimal example feature computations for MVP.
  order_history: list of dicts with 'date' and 'quantity'
  """
  if not order_history:
    return {"recency_days": 999, "purchase_frequency": 0, "avg_qty": 0}
  # placeholder computations
  recency_days = 30
  purchase_frequency = len(order_history)
  avg_qty = sum([o.get("quantity", 1) for o in order_history]) / max(1, purchase_frequency)
  return {
    "recency_days": recency_days,
    "purchase_frequency": purchase_frequency,
    "avg_qty": avg_qty
  }
  