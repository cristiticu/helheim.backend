
from datetime import datetime, timezone
from uuid import uuid4
from pwdlib import PasswordHash
from pydantic import UUID4
from accounts.exceptions import AccountNotFound, UsernameAlreadyExists
from accounts.model import Account, CreateAccount
from accounts.persistence import AccountsPersistence


pwd_context = PasswordHash.recommended()


class AccountsService():
    def __init__(self, accounts: AccountsPersistence):
        self._accounts = accounts

    def get(self, guid: UUID4):
        account = self._accounts.get(guid)
        return account.to_dto()

    def create(self, payload: CreateAccount):
        try:
            self._accounts.get_by_username(payload.username)
            raise UsernameAlreadyExists()
        except AccountNotFound:
            pass

        account_payload = {
            **payload.model_dump(exclude_none=True),
            "guid": uuid4(),
            "password": pwd_context.hash(payload.password),
            "c_at": datetime.now(timezone.utc)
        }

        account = Account.model_validate(account_payload)
        self._accounts.persist(account)

        return account.to_dto()

    def delete(self, guid: UUID4):
        self._accounts.delete(guid)
