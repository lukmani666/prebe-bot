from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import routes_webhook, routes_customers, routes_predictions, routes_events
from app.db.base import Base
from app.db.session import engine

#create DB tables for MVP (I will use Alembic for production migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(
  title="PreBe Bot Backend",
  description="FastAPI backend for PreBe predictive WhatsApp automation",
  version="0.1.0",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.BACKEND_CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(routes_webhook.router, prefix="/api/v1/webhook", tags=["webhook"])
app.include_router(routes_customers.router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(routes_predictions.router, prefix="/api/v1/predictions", tags=["predictions"])
app.include_router(routes_events.router, prefix="/api/v1/events", tags=["events"])

@app.get("/health", tags=["health"])
def health_check():
  return {"status": "ok"}
