import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_s3_client():
  session = boto3.session.Session()
  client = session.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name="us-east-1"
  )
  return client

def upload_bytes(bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
  client = get_s3_client()
  try:
    client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    url = f"{settings.S3_ENDPOINT_URL}/{bucket}/{key}"
    return url
  except ClientError:
    logger.exception("Failed to upload to S3")
    raise