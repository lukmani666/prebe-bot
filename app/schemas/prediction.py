from pydantic import BaseModel
from typing import Optional, Any

class NextPurchaseResponse(BaseModel):
  days_until_next_purchase: int
  confidence: Optional[float] = None