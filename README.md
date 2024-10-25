# S3 Proxy Service

FastAPI-based proxy service for AWS S3 upload and download operations.

## Features

- File upload to S3 buckets
- File download from S3 buckets

### API Endpoints

1. Upload file:
  /upload/?bucket_name=my-bucket&object_name=path/to/file.txt

2. Download file:
  "/download/?bucket_name=my-bucket&object_name=path/to/file.txt"
