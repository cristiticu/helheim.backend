from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import UUID4
from auth.dependencies import UserTokenDependency
from context import ApplicationContext, get_application_context
from realms.dependencies import RealmUserDependency, RealmUserRoleFactory
from realms.model import CloseRealmPortal, CreateRealmFile, CreateRealmPortal, CreateRealmWorldBackup


router = APIRouter(prefix="/realm", tags=["Realms"])


@router.get("")
def get_user_realms(
    token: UserTokenDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    realms = ctx.realms.get_realms_for_user(token.user_guid)
    return realms


@router.get("/{guid}")
def get_realm(
    guid: UUID4,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    realm = ctx.realms.get_realm(guid)
    return realm


@router.get("/{guid}/user")
def get_realm_users(
    guid: UUID4,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    users = ctx.realms.get_realm_users(guid)
    return users


@router.get("/{guid}/file/{file_name}")
def get_realm_file(
    guid: UUID4,
    file_name: str,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    return ctx.realms.get_realm_list_file(guid, file_name)


@router.post("/{guid}/file", dependencies=[Depends(RealmUserRoleFactory(["admin"]))])
def create_list_file(
    guid: UUID4,
    payload: CreateRealmFile,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    ctx.realms.save_realm_list_file(guid, payload)

    return {"message": "File created successfully"}


@router.get("/{guid}/world")
def get_realm_worlds(
    guid: UUID4,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    worlds = ctx.realms.get_realm_worlds(guid)
    return worlds


@router.post("/{guid}/world/{world_name}/backup", dependencies=[Depends(RealmUserRoleFactory(["admin"]))])
def create_world_backup(
    guid: UUID4,
    world_name: str,
    payload: CreateRealmWorldBackup,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    ctx.realms.create_world_backup(
        guid, world_name, payload.backup_name)

    return {"message": "Backup created successfully"}


@router.delete("/{guid}/world/{world_name}", dependencies=[Depends(RealmUserRoleFactory(["admin"]))])
def delete_realm_world(
    guid: UUID4,
    world_name: str,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    ctx.realms.delete_world(guid, world_name)

    return {"message": "World deleted successfully"}


@router.get("/{guid}/portal")
def get_realm_portals(
    guid: UUID4,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    portals = ctx.realms.get_realm_portals(guid)
    return portals


@router.post("/{guid}/portal")
def open_realm_portal(
    guid: UUID4,
    payload: CreateRealmPortal,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    portal = ctx.realms.open_portal(
        guid, realm_user.guid, payload)
    return portal


@router.delete("/{guid}/portal")
def close_realm_portal(
    guid: UUID4,
    payload: CloseRealmPortal,
    realm_user: RealmUserDependency,
    ctx: Annotated[ApplicationContext, Depends(get_application_context)],
):
    ctx.realms.close_portal(guid, payload)

    return {"message": "Portal closed successfully"}
