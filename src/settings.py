import json
from dotenv import load_dotenv
import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", None)


if ENVIRONMENT is None:
    raise ValueError(
        "ENVIRONMENT variable is not set. Please set it to 'local', 'production' or 'test.")
elif ENVIRONMENT == "local":
    load_dotenv('.env.local')
elif ENVIRONMENT == "production":
    load_dotenv('.env.production')
elif ENVIRONMENT == "test":
    load_dotenv('.env.test')
else:
    raise ValueError(
        f"Invalid ENVIRONMENT value: {ENVIRONMENT}. Must be 'local', 'production' or 'test'.")

AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL')

CORS_ORIGINS = json.loads(
    os.environ.get('CORS_ORIGINS', '[]'))

AUTH_TABLE_NAME = "helheim.table.authentication"
AUTH_TABLE_USERNAME_GSI = "gsi.username"

REALMS_TABLE_NAME = "helheim.table.realms"
REALMS_TABLE_USER_GUID_GSI = "gsi.user-realms-lookup-2"

REALM_STORAGE_S3_BUCKET_NAME = "helheim.storage"

VALHEIM_INSTANCE_LAMBDA_NAME = "helheim_instance_lambda"
VINTAGE_STORY_INSTANCE_LAMBDA_NAME = "helheim_vintage_story_instance_lambda"

SECRET_KEY = "b386aaadd83435c99d40d96234972bf3330506473c6a41d081565a6cc39d1b7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
