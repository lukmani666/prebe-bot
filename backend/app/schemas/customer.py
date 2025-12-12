from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from uuid import UUID

class CustomerBase(BaseModel):
  phone: str
  name: Optional[str] = None
  email: Optional[str] = None
  locale: Optional[str] = None
  timezone: Optional[str] = None
  mata: Optional[Dict[str, Any]] = {}

class CustomerCreate(CustomerBase):
  pass

class CustomerRead(CustomerBase):
  id: UUID
  created_at: Optional[str] = None

  model_config = {
    "from_attributes": True
  }