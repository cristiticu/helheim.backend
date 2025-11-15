from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import UUID4
from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from realms.dependencies import realm_user_data
from realms.model import CloseRealmPortal, CreateRealmPortal, RealmUser


router = APIRouter(prefix="/realm", tags=["Realms"])
application_context = ApplicationContext()


@router.get("")
def get_user_realms(token: Annotated[UserTokenData, Depends(user_token_data)]):
    realms = application_context.realms.get_realms_for_user(token.user_guid)
    return realms


@router.get("/{guid}")
def get_realm(guid: UUID4, realm_user: Annotated[RealmUser, Depends(realm_user_data)]):
    realm = application_context.realms.get_realm(guid)
    return realm


@router.get("/{guid}/users")
def get_realm_users(guid: UUID4, realm_user: Annotated[RealmUser, Depends(realm_user_data)]):
    users = application_context.realms.get_realm_users(guid)
    return users


@router.get("/{guid}/portals")
def get_realm_portals(guid: UUID4, realm_user: Annotated[RealmUser, Depends(realm_user_data)]):
    portals = application_context.realms.get_realm_portals(guid)
    return portals


@router.get("/{guid}/worlds")
def get_realm_worlds(guid: UUID4, realm_user: Annotated[RealmUser, Depends(realm_user_data)]):
    worlds = application_context.realms.get_realm_worlds(guid)
    return worlds


@router.post("/{guid}/portals")
def open_realm_portal(guid: UUID4, payload: CreateRealmPortal, realm_user: Annotated[RealmUser, Depends(realm_user_data)]):
    portal = application_context.realms.open_portal(guid, payload)
    return portal


@router.delete("/{guid}/portals")
def close_realm_portal(guid: UUID4, payload: CloseRealmPortal, realm_user: Annotated[RealmUser, Depends(realm_user_data)]):
    application_context.realms.close_portal(guid, payload)
