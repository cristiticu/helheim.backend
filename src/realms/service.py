from datetime import datetime, timezone
import json
import logging
from uuid import uuid4
from pydantic import UUID4
import settings
from realms.exceptions import InvalidRealmListFileName, PasswordTooShort, PortalAlreadyOpened
from realms.model import CloseRealmPortal, CreateRealmFile, CreateRealmPortal, Realm, RealmPortal, RealmWorld, ValheimWorldModifier, VintageStoryWorldModifier
from realms.persistence import RealmsPersistence
from shared.ec2 import ec2_client
from shared.lambda_client import lambda_client


class RealmsService():
    def __init__(self, realms: RealmsPersistence):
        self._realms = realms
        self._lambda = lambda_client()
        self._ec2 = ec2_client()
        self._logger = logging.getLogger(__name__)

    def get_realm(self, guid: UUID4):
        self._logger.debug(f"Fetching realm with guid: {guid}")
        return self._realms.get_realm(guid)

    def get_realms_for_user(self, user_guid: UUID4):
        return self._realms.get_realms_for_user(user_guid)

    def get_realm_user(self, realm_guid: UUID4, user_guid: UUID4):
        return self._realms.get_realm_user(realm_guid, user_guid)

    def get_realm_users(self, guid: UUID4):
        return self._realms.get_realm_users(guid)

    def get_realm_portals(self, guid: UUID4):
        return self._realms.get_realm_portals(guid)

    def get_realm_worlds(self, guid: UUID4) -> list[RealmWorld]:
        return self._realms.get_realm_worlds(guid)

    def create_world_backup(self, realm_guid: UUID4, world_name: str, backup_name: str):
        self._logger.info(
            f"Creating world backup for realm {realm_guid}, world: {world_name}, backup: {backup_name}")
        self._realms.persist_world_backup(realm_guid, world_name, backup_name)
        self._logger.info(f"Successfully created world backup: {backup_name}")

    def delete_world(self, realm_guid: UUID4, world_name: str):
        self._logger.warning(
            f"Deleting world '{world_name}' from realm {realm_guid}")
        self._realms.delete_world(realm_guid, world_name)
        self._logger.info(f"Successfully deleted world: {world_name}")

    def get_realm_list_file(self, realm_guid: UUID4, file_name: str):
        return self._realms.get_realm_list_file(realm_guid, file_name)

    def save_realm_list_file(self, realm_guid: UUID4, payload: CreateRealmFile):
        self._logger.info(
            f"Saving realm list file '{payload.file_name}' for realm {realm_guid}")

        if payload.file_name not in ["permittedlist.txt", "bannedlist.txt", "adminlist.txt"]:
            self._logger.error(
                f"Invalid realm list file name: {payload.file_name}")
            raise InvalidRealmListFileName()

        self._realms.persist_realm_list_file(realm_guid, payload)
        self._logger.info(
            f"Successfully saved realm list file: {payload.file_name}")

    def invoke_valheim_instance_lambda(self, realm: Realm, payload: CreateRealmPortal):
        valheim_modifiers = [
            modifier.model_dump()
            for modifier in payload.modifiers
            if isinstance(modifier, ValheimWorldModifier.__args__)
        ] if payload.modifiers else None

        lambda_payload = {
            "realmGuid": str(realm.guid),
            "serverName": payload.name,
            "worldName": payload.world_name,
            "password": payload.password,
            "preset": payload.preset,
            "modifiers": valheim_modifiers,
            "keys": payload.keys,
            "modpack": payload.modpack,
        }

        self._logger.info(
            f"Invoking instance lambda for realm {realm.name} ({realm.guid})")
        response = self._lambda.invoke(
            FunctionName=settings.VALHEIM_INSTANCE_LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload)
        )

        response_payload = json.loads(
            response.get("Payload").read().decode("utf-8"))

        return response_payload

    def invoke_vintage_story_instance_lambda(self, realm: Realm, payload: CreateRealmPortal):
        vintage_story_modifiers = [
            modifier.model_dump()
            for modifier in payload.modifiers
            if isinstance(modifier, VintageStoryWorldModifier.__args__)
        ] if payload.modifiers else None

        lambda_payload = {
            "realmGuid": str(realm.guid),
            "serverName": payload.name,
            "worldName": payload.world_name,
            "password": payload.password,
            "modpack": payload.modpack,
            "modifiers": vintage_story_modifiers,
        }

        self._logger.info(
            f"Invoking Vintage Story instance lambda for realm {realm.name} ({realm.guid})")
        response = self._lambda.invoke(
            FunctionName=settings.VINTAGE_STORY_INSTANCE_LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload)
        )

        response_payload = json.loads(
            response.get("Payload").read().decode("utf-8"))

        return response_payload

    def open_portal(self, realm_guid: UUID4, user_guid: UUID4, payload: CreateRealmPortal):
        self._logger.info(
            f"Opening portal for realm {realm_guid} by user {user_guid}, server: {payload.name}")

        realm = self.get_realm(realm_guid)
        opened_portals = self.get_realm_portals(realm.guid)

        if len(opened_portals) > 0:
            self._logger.warning(
                f"Portal already opened for realm {realm_guid}")
            raise PortalAlreadyOpened()

        if len(payload.password) < 6:
            self._logger.warning(
                f"Password too short for realm {realm_guid} portal")
            raise PasswordTooShort()

        if realm.realm_type == "valheim":
            response_payload = self.invoke_valheim_instance_lambda(
                realm, payload)
        elif realm.realm_type == "vintage_story":
            response_payload = self.invoke_vintage_story_instance_lambda(
                realm, payload)
        else:
            self._logger.error(
                f"Unsupported realm type '{realm.realm_type}' for realm {realm_guid}")
            raise Exception(
                f"Unsupported realm type: {realm.realm_type}")

        self._logger.info(
            f"Instance created successfully - ID: {response_payload.get('instanceId')}, IP: {response_payload.get('publicIpAddress')}")

        portal_payload = {
            "guid": realm_guid,
            "portal_guid": uuid4(),
            "opened_by_user_guid": user_guid,

            "instance_id": response_payload["instanceId"],
            "spot_request_id": response_payload["spotRequestId"],
            "name": response_payload["config"]["serverName"],
            "world_name": response_payload["config"]["worldName"],
            "password": payload.password,
            "public_address": response_payload["publicIpAddress"],
            "region": response_payload["region"],
            "instance_type": response_payload["instanceType"],
            "status": response_payload["status"],
            "c_at": datetime.now(timezone.utc),
            "meta_type": "REALM_PORTAL",
        }

        portal = RealmPortal.model_validate(portal_payload)

        self._realms.persist(portal)

        self._logger.info(
            f"Portal successfully opened for realm {realm_guid} - Portal ID: {portal.portal_guid}")
        return portal

    def close_portal(self, realm_guid: UUID4, payload: CloseRealmPortal):
        self._logger.info(
            f"Closing portal for realm {realm_guid} - Portal ID: {payload.portal_guid}")

        try:
            self._ec2.terminate_instances(
                InstanceIds=[payload.instance_id],
                Force=False,
                SkipOsShutdown=False
            )
            self._logger.info(
                f"Successfully initiated termination of EC2 instance: {payload.instance_id}")
        except Exception as e:
            self._logger.warning(
                f"Failed to terminate EC2 instance {payload.instance_id}: {str(e)}. "
                "Instance may already be terminated."
            )

        try:
            self._ec2.cancel_spot_instance_requests(
                SpotInstanceRequestIds=[payload.spot_request_id]
            )
            self._logger.info(
                f"Successfully cancelled spot instance request: {payload.spot_request_id}")
        except Exception as e:
            self._logger.warning(
                f"Failed to cancel spot instance request {payload.spot_request_id}: {str(e)}. "
                "Request may already be cancelled."
            )

        self._realms.delete_portal(realm_guid, payload.portal_guid)
        self._logger.info(f"Portal successfully closed for realm {realm_guid}")
