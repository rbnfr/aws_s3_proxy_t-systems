from typing import Optional, BinaryIO
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from core.logging import get_logger

logger = get_logger()


class S3Client:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    async def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        file_content: BinaryIO,
        content_type: str,
        metadata: Optional[dict] = None
    ) -> dict:
        """Upload a file to S3"""
        try:
            self._verify_bucket(bucket_name)

            full_metadata = {
                'uploaded_at': datetime.now().isoformat(),
                **(metadata or {})
            }

            self.client.put_object(
                Bucket=bucket_name,
                Key=object_name,
                Body=file_content,
                ContentType=content_type,
                Metadata=full_metadata
            )

            logger.info(f"Successfully uploaded {object_name} to {bucket_name}")

            return {
                "status": "success",
                "bucket": bucket_name,
                "object": object_name,
                "content_type": content_type,
                "metadata": full_metadata
            }

        except ClientError as e:
            self._handle_client_error(e, "upload", bucket_name, object_name)

    async def download_file(self, bucket_name: str, object_name: str) -> tuple:
        """Download a file from S3"""
        try:
            self._verify_bucket(bucket_name)

            response = self.client.get_object(
                Bucket=bucket_name,
                Key=object_name
            )

            logger.info(f"Successfully downloaded {object_name} from {bucket_name}")

            return (
                response['Body'].read(),
                response.get('ContentType', 'application/octet-stream'),
                response.get('Metadata', {})
            )

        except ClientError as e:
            self._handle_client_error(e, "download", bucket_name, object_name)

    def list_buckets(self) -> list:
        """List all S3 buckets"""
        try:
            response = self.client.list_buckets()
        except ClientError as e:
            self._handle_client_error(e, "list buckets", bucket_name="N/A", object_name="N/A")

        buckets = [bucket['Name'] for bucket in response['Buckets']]

        return buckets

    def _verify_bucket(self, bucket_name: str) -> None:
        """Verify bucket exists and is accessible"""
        try:
            self.client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            self._handle_client_error(e, "verify", bucket_name)

    def _handle_client_error(
        self,
        error: ClientError,
        operation: str,
        bucket_name: str,
        object_name: Optional[str] = None
    ) -> None:
        """TODO Handle AWS client errors and raise appropriate custom exceptions"""
        error_code = error.response['Error']['Code']

        raise ClientError(
            f"AWS S3 error: {error_code}, \
            {operation} failed, \
            bucket: {bucket_name}, \
            object: {object_name}"
        )
