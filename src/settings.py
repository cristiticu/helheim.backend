import json
from dotenv import load_dotenv
import os

load_dotenv('.env')

AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')
CORS_ORIGINS = json.loads(
    os.environ.get('CORS_ORIGINS', '[]'))

AUTH_TABLE_NAME = "helheim.table.authentication"
AUTH_TABLE_USERNAME_GSI = "gsi.username"

REALMS_TABLE_NAME = "helheim.table.realms"
REALMS_TABLE_USER_GUID_GSI = "gsi.user-realms-lookup-2"

REALM_WORLDS_S3_BUCKET_NAME = "helheim.storage"

INSTANCE_LAMBDA_NAME = "helheim_instance_lambda"

SECRET_KEY = "b386aaadd83435c99d40d96234972bf3330506473c6a41d081565a6cc39d1b7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
