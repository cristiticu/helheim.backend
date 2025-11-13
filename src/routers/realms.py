from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import UUID4

from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext
from realms.model import CloseRealmPortal, CreateRealmPortal


router = APIRouter(prefix="/realm", tags=["Realms"])
application_context = ApplicationContext()


@router.get("")
def get_user_realms(token: Annotated[UserTokenData, Depends(user_token_data)]):
    realms = application_context.realms.get_realms_for_user(token.user_guid)
    return realms


@router.get("/{guid}")
def get_realm(guid: UUID4, token: Annotated[UserTokenData, Depends(user_token_data)]):
    realm = application_context.realms.get_realm(guid)
    return realm


@router.get("/{guid}/users")
def get_realm_users(guid: UUID4, token: Annotated[UserTokenData, Depends(user_token_data)]):
    users = application_context.realms.get_realm_users(guid)
    return users


@router.get("/{guid}/portals")
def get_realm_portals(guid: UUID4, token: Annotated[UserTokenData, Depends(user_token_data)]):
    portals = application_context.realms.get_realm_portals(guid)
    return portals


@router.post("/{guid}/portals")
def open_realm_portal(guid: UUID4, payload: CreateRealmPortal, token: Annotated[UserTokenData, Depends(user_token_data)]):
    portal = application_context.realms.open_portal(guid, payload)
    return portal


@router.delete("/{guid}/portals")
def close_realm_portal(guid: UUID4, payload: CloseRealmPortal, token: Annotated[UserTokenData, Depends(user_token_data)]):
    application_context.realms.close_portal(guid, payload)
