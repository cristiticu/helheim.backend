import base64
from datetime import datetime
import json


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
