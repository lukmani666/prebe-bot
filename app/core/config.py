from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from typing import List
from decouple import config

class Settings(BaseSettings):
  #App
  APP_NAME: str = "PreBe Bot Backend"
  BACKEND_CORS_ORIGIN: List[str] = ["*"] # tighten in production

  #Postgres config
  POSTGRES_USER: str = config("POSTGRES_USER")
  POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD")
  POSTGRES_DB: str = config("POSTGRES_DB")
  POSTGRES_HOST: str = config("POSTGRES_HOST")
  POSTGRES_PORT: str = config("POSTGRES_PORT")

  #redis config
  REDIS_URL: str = config("REDIS_URL")

  #MinIo / S3
  S3_ENDPOINT_URL: str = config("S3_ENDPOINT_URL")
  S3_ACCESS_KEY: str = config("S3_ACCESS_KEY")
  S3_SECRET_KEY: str = config("S3_SECRET_KEY")
  S3_BUCKET: str = config("S3_BUCKET")

  #WhatsApp
  WHATSAPP_TOKEN: str = ""

  #ML models folder
  ML_MODELS_PATH: str = "/app/ml/models"

  #Celery (broker / backend)
  CELERY_BROKER_URL: str = config("CELERY_BROKER_URL")
  CELERY_RESULT_BACKEND: str = config("CELERY_RESULT_BACKEND")

  class Config:
    env_file = ".env"
    case_sensitive = True

settings = Settings()