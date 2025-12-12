from sqlalchemy.orm import Session
from app.db.models.customer import Customer
from app.schemas.customer import CustomerCreate
from typing import List, Optional
import uuid

class CustomerRepository:
  def __init__(self, db: Session):
    self.db = db
  
  def create(self, payload: CustomerCreate) -> Customer:
    obj = Customer(
      id=uuid.uuid4(),
      phone=payload.phone,
      email=payload.email,
      locale=payload.locale,
      timezone=payload.timezone,
      meta=payload.meta or {},
    )
    self.db.add(obj)
    self.db.commit()
    self.db.refresh(obj)
    return obj
  
  def get_by_id(self, customer_id: str) -> Optional[Customer]:
    return self.db.query(Customer).filter(Customer.id == customer_id).first()
  
  def list(self, limit: int = 20) -> List[Customer]:
    return self.db.query(Customer).order_by(Customer.created_at.desc()).limit(limit).all()
  
  def get_by_phone(self, phone: str) -> Optional[Customer]:
    return self.db.query(Customer).filter(Customer.phone == phone).first()