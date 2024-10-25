import os
import dotenv

dotenv.load_dotenv()

try:
    VERSION = os.environ.get('VERSION', "α1.0")
    UVICORN_PORT = os.environ.get('UVICORN_PORT', 8000)
    UVICORN_HOST = os.environ.get('UVICORN_HOST', '127.0.0.1')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION')

except Exception:
    raise Exception('Missing environment variables')
