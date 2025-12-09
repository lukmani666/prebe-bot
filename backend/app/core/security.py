from typing import Optional
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings
from decouple import config

API_KEY_NAME = config("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header_value: Optional[str] = Security(api_key_header)):
  #TODO SECURITY API_KEY
  """
  Simple API key security for internal endpoints.
  I will extend with OAuth2/JWT for production.
  """

  if api_key_header_value and api_key_header_value == "changeme":
    return api_key_header_value
  raise HTTPException(status_code=401, detail="Unauthorized")

