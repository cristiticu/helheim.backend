from typing import Annotated
from fastapi import Depends
from pydantic import UUID4
from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from exceptions import CredentialsException
from realms.exceptions import RealmUserNotFound
from realms.model import RealmUser

application_context = ApplicationContext()


def realm_user_data(guid: UUID4, token: Annotated[UserTokenData, Depends(user_token_data)]) -> RealmUser:
    try:
        return application_context.realms.get_realm_user(guid, token.user_guid)
    except RealmUserNotFound:
        raise CredentialsException(
            msg="User does not have access to this realm")
