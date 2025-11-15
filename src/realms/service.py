from datetime import datetime, timezone
import json
from uuid import uuid4
from pydantic import UUID4
import settings
from realms.exceptions import PasswordTooShort, PortalAlreadyOpened
from realms.model import CloseRealmPortal, CreateRealmPortal, RealmPortal
from realms.persistence import RealmsPersistence
from shared.ec2 import ec2_client
from shared.lambda_client import lambda_client
from shared.s3 import s3_client


class RealmsService():
    def __init__(self, realms: RealmsPersistence):
        self._realms = realms
        self._lambda = lambda_client()
        self._ec2 = ec2_client()
        self._s3 = s3_client()

    def get_realm(self, guid: UUID4):
        return self._realms.get_realm(guid)

    def get_realms_for_user(self, user_guid: UUID4):
        return self._realms.get_realms_for_user(user_guid)

    def get_realm_user(self, realm_guid: UUID4, user_guid: UUID4):
        return self._realms.get_realm_user(realm_guid, user_guid)

    def get_realm_users(self, guid: UUID4):
        return self._realms.get_realm_users(guid)

    def get_realm_portals(self, guid: UUID4):
        return self._realms.get_realm_portals(guid)

    def get_realm_worlds(self, guid: UUID4) -> list[str]:
        search_prefix = f"{guid}/worlds/"
        delimiter = "/"

        world_names = []

        response = self._s3.list_objects_v2(
            Bucket=settings.REALM_WORLDS_S3_BUCKET_NAME,
            Prefix=search_prefix,
            Delimiter=delimiter,
        )

        for prefix in response.get("CommonPrefixes", []):
            full_prefix = prefix.get("Prefix", "")

            world_name = full_prefix.replace(
                search_prefix, "").rstrip(delimiter)

            if world_name:
                world_names.append(world_name)

        return world_names

    def open_portal(self, realm_guid: UUID4, payload: CreateRealmPortal):
        realm = self.get_realm(realm_guid)
        opened_portals = self.get_realm_portals(realm.guid)

        if len(opened_portals) > 0:
            raise PortalAlreadyOpened()

        if len(payload.password) < 6:
            raise PasswordTooShort()

        lambda_payload = {
            "realmGuid": str(realm_guid),
            "serverName": payload.name,
            "worldName": payload.world_name,
            "password": payload.password
        }

        response = self._lambda.invoke(
            FunctionName=settings.INSTANCE_LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload)
        )

        response_payload = json.loads(
            response.get("Payload").read().decode("utf-8"))
        portal_payload = {
            "guid": realm_guid,
            "portal_guid": uuid4(),

            "instance_id": response_payload["instanceId"],
            "spot_request_id": response_payload["spotRequestId"],
            "name": response_payload["config"]["serverName"],
            "world_name": response_payload["config"]["worldName"],
            "public_address": response_payload["publicIpAddress"],
            "region": response_payload["region"],
            "instance_type": response_payload["instanceType"],
            "status": response_payload["status"],
            "c_at": datetime.now(timezone.utc),
            "meta_type": "REALM_PORTAL",
        }

        portal = RealmPortal.model_validate(portal_payload)

        self._realms.persist(portal)

        return portal

    def close_portal(self, realm_guid: UUID4, payload: CloseRealmPortal):
        self._ec2.terminate_instances(
            InstanceIds=[payload.instance_id],
            Force=False,
            SkipOsShutdown=False
        )

        self._ec2.cancel_spot_instance_requests(
            SpotInstanceRequestIds=[payload.spot_request_id]
        )

        self._realms.delete_portal(realm_guid, payload.portal_guid)
