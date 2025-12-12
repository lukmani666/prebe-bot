from typing import Dict
import logging

logger = logging.getLogger(__name__)

class SentimentService:
  """
  Lightweight sentiment analysis wrapper. Replace with HF model for production.
  """
  def __init__(self):
    # optionally load a lightweight model or sentiment lexicon
    pass

  def analyze(self, text: str) -> Dict[str, float]:
    """
    Return sentiment scores and a label.
    Simple heuristic placeholder: positive if contains common words.
    """
    text_lower = (text or "").lower()
    score = 0.0
    if any(w in text_lower for w in ["thanks", "great", "love", "good"]):
      score = 0.8
    elif any(w in text_lower for w in ["bad", "hate", "angry", "not happy", "terrible"]):
      score = -0.6
    return {"score": score, "label": "positive" if score > 0 else "negative" if score < 0 else "neutral"}