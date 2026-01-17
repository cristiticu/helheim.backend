import base64
from datetime import datetime
import json
import settings


def format_utc_datetime_string(utc_datetime: datetime):
    return utc_datetime.isoformat().replace("+00:00", "Z")


def encode_last_evaluated_key(key):
    json_str = json.dumps(key)
    base64_str = base64.urlsafe_b64encode(json_str.encode()).decode()

    return base64_str


def decode_last_evaluated_key(base64_key: str):
    json_str = base64.urlsafe_b64decode(s=base64_key.encode()).decode()
    key = json.loads(json_str)

    return key


def get_aws_env_params():
    params = {}

    # In production, we rely on the IAM role assigned to the instance/container
    if settings.ENVIRONMENT == "production":
        return params

    if hasattr(settings, 'AWS_REGION_NAME') and settings.AWS_REGION_NAME:
        params['region_name'] = settings.AWS_REGION_NAME

    if hasattr(settings, 'AWS_ENDPOINT_URL') and settings.AWS_ENDPOINT_URL:
        params['endpoint_url'] = settings.AWS_ENDPOINT_URL

    if getattr(settings, 'AWS_ACCESS_KEY_ID', None) and getattr(settings, 'AWS_SECRET_ACCESS_KEY', None):
        params['aws_access_key_id'] = settings.AWS_ACCESS_KEY_ID
        params['aws_secret_access_key'] = settings.AWS_SECRET_ACCESS_KEY

    return params
