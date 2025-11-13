from pwdlib import PasswordHash, hashers
from pydantic import UUID4
from auth.utils import create_access_token, decode_access_token
from exceptions import CredentialsException
import settings
from accounts.exceptions import AccountNotFound
from accounts.persistence import AccountsPersistence


pwd_context = PasswordHash.recommended()


class AuthService():
    def __init__(self, accounts: AccountsPersistence):
        self._accounts = accounts

    def create_tokens(self, user_guid: UUID4):
        access_token = create_access_token(
            {"user_guid": str(user_guid)}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = create_access_token(
            {
                "user_guid": str(user_guid),
            }, settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def authenticate(self, username: str, password: str):
        try:
            user = self._accounts.get_by_username(username)
        except AccountNotFound:
            raise CredentialsException(msg="Invalid credentials")

        if not pwd_context.verify(password, user.password):
            raise CredentialsException(msg="Invalid credentials")

        return self.create_tokens(user.guid)

    def refresh(self, refresh_token: str, user_guid: UUID4):
        token_data = decode_access_token(refresh_token)

        if token_data.get("user_guid") != user_guid:
            raise CredentialsException(msg="Invalid credentials")

        new_access_token = create_access_token(
            {"user_guid": str(user_guid)},
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        new_refresh_token = create_access_token({
            "user_guid": str(user_guid)},
            settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
