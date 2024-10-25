from fastapi import APIRouter, UploadFile, HTTPException, Depends, File
from fastapi.responses import StreamingResponse
from botocore.exceptions import ClientError
from datetime import datetime

from services.s3 import S3Client
from core.logging import get_logger
from api.dependencies import get_s3_client

logger = get_logger()
router = APIRouter()


@router.get("/")
async def home(s3_client: S3Client = Depends(get_s3_client)):
    """
    Home endpoint that also verifies AWS credentials and S3 connection
    """
    try:
        # Try to list buckets to verify AWS credentials
        buckets = s3_client.list_buckets()
        return {
            "status": "healthy",
            "aws_connection": "ok",
            "timestamp": datetime.now().isoformat(),
            "buckets": buckets
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service unhealthy - AWS connection failed"
        )


@router.post("/upload/")
async def upload_file(
    bucket_name: str,
    object_name: str,
    file: UploadFile = File(...),
    s3_client: S3Client = Depends(get_s3_client)
):
    try:
        contents = await file.read()
        metadata = {
            'original_filename': file.filename,
            'content_type': file.content_type
        }

        result = await s3_client.upload_file(
            bucket_name=bucket_name,
            object_name=object_name,
            file_content=contents,
            content_type=file.content_type,
            metadata=metadata
        )

        return result

    except ClientError as e:
        logger.error(f"S3 Proxy error: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/")
async def download_file(
    bucket_name: str,
    object_name: str,
    s3_client: S3Client = Depends(get_s3_client)
):
    try:
        content, content_type, _ = await s3_client.download_file(
            bucket_name=bucket_name,
            object_name=object_name
        )

        return StreamingResponse(
            iter([content]),
            media_type=content_type,
            headers={'Content-Disposition': f'attachment; filename="{object_name}"'}
        )

    except ClientError as e:
        logger.error(f"S3 Proxy error: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
