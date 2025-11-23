from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, ExpiredSignatureError
from auth.utils import decode_access_token
from auth.model import RefreshTokenData, UserTokenData
from exceptions import CredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


def user_token_data(token: Annotated[str, Depends(oauth2_scheme)]) -> UserTokenData:
    try:
        payload = decode_access_token(token)
        user_guid = payload.get("user_guid")

        if user_guid is None:
            raise CredentialsException()

    except ExpiredSignatureError:
        raise CredentialsException(msg="Expired signature")
    except InvalidTokenError:
        raise CredentialsException(msg="Corrupt signature")

    return UserTokenData(raw_token=token, user_guid=user_guid)


def user_token_query(token: str) -> UserTokenData:
    try:
        payload = decode_access_token(token)
        user_guid = payload.get("user_guid")

        if user_guid is None:
            raise CredentialsException()

    except ExpiredSignatureError:
        raise CredentialsException(msg="Expired signature")
    except InvalidTokenError:
        raise CredentialsException(msg="Corrupt signature")

    return UserTokenData(raw_token=token, user_guid=user_guid)


def refresh_token_data(refresh_token: Annotated[str, Depends(oauth2_scheme)]) -> RefreshTokenData:
    try:
        payload = decode_access_token(refresh_token)
        user_guid = payload.get("user_guid")

        if user_guid is None:
            raise CredentialsException()

    except ExpiredSignatureError:
        raise CredentialsException(msg="Expired signature")
    except InvalidTokenError:
        raise CredentialsException(msg="Corrupt signature")

    return RefreshTokenData(raw_token=refresh_token, user_guid=user_guid)


UserTokenDependency = Annotated[UserTokenData, Depends(user_token_data)]
RefreshTokenDependency = Annotated[RefreshTokenData, Depends(
    refresh_token_data)]
