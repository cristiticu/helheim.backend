from typing import Annotated
from fastapi import Depends
from pydantic import UUID4
from auth.dependencies import UserTokenDependency
from context import ApplicationContext
from realms.exceptions import InsufficientRealmPermissions, RealmUserNotFound
from realms.model import RealmUser

application_context = ApplicationContext()


def realm_user_data(guid: UUID4, token: UserTokenDependency) -> RealmUser:
    try:
        return application_context.realms.get_realm_user(guid, token.user_guid)
    except RealmUserNotFound:
        raise InsufficientRealmPermissions(
            msg="User does not have access to this realm")


def RealmUserRoleFactory(required: list[str]):
    def validator(realm_user: RealmUserDependency):
        if realm_user.role not in required:
            raise InsufficientRealmPermissions

    return validator


RealmUserDependency = Annotated[RealmUser, Depends(realm_user_data)]
