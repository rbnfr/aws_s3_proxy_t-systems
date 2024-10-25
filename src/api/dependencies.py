from functools import lru_cache

from config.settings import get_settings
from services.s3 import S3Client


@lru_cache()
def get_s3_client() -> S3Client:
    settings = get_settings()
    return S3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
