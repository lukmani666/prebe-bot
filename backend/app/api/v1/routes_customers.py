from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.customer import CustomerCreate, CustomerRead
from app.db.repositories.customer_repo import CustomerRepository
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=CustomerRead)
def create_customer(payload: CustomerCreate, db=Depends(get_db)):
  repo = CustomerRepository(db)
  customer = repo.create(payload)
  return customer

@router.get("/", response_model=List[CustomerRead])
def list_customers(limit: int = 20, db=Depends(get_db)):
  repo = CustomerRepository(db)
  return repo.list(limit=limit)

@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: str, db=Depends(get_db)):
  repo = CustomerRepository(db)
  customer = repo.get_by_id(customer_id)
  if not customer:
    raise HTTPException(status_code=404, detail="Customer not found")
  return customer