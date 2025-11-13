from datetime import datetime, timedelta, timezone
import jwt
import settings


def create_access_token(data: dict, expire: int):
    expire_delta = timedelta(minutes=expire)
    encode = data.copy()
    expires_at = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expires_at})

    return jwt.encode(encode, settings.SECRET_KEY, settings.ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
