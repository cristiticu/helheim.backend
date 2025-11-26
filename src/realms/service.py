from datetime import datetime, timezone
import json
from uuid import uuid4
from botocore.exceptions import ClientError
from pydantic import UUID4
from exceptions import InvalidItemRequest
import settings
from realms.exceptions import InvalidRealmListFileName, PasswordTooShort, PortalAlreadyOpened, RealmListFileNotFound, WorldNotFound
from realms.model import CloseRealmPortal, CreateRealmFile, CreateRealmPortal, RealmListFile, RealmPortal, RealmWorld
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

    def get_realm_worlds(self, guid: UUID4) -> list[RealmWorld]:
        search_prefix = f"{guid}/worlds/"
        delimiter = "/"

        world_names = []

        response = self._s3.list_objects_v2(
            Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
            Prefix=search_prefix,
            Delimiter=delimiter,
        )

        for prefix in response.get("CommonPrefixes", []):
            full_prefix = prefix.get("Prefix", "")

            world_name = full_prefix.replace(
                search_prefix, "").rstrip(delimiter)

            if world_name:
                world_names.append(world_name)

        realm_worlds = []

        for world_name in world_names:
            realm_world_key = f"{guid}/worlds/{world_name}/{world_name}.db"

            response = self._s3.head_object(
                Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
                Key=realm_world_key
            )

            last_modified = response.get("LastModified")

            realm_world_payload = {
                "name": world_name,
                "m_at": last_modified
            }

            realm_world = RealmWorld.model_validate(realm_world_payload)

            realm_worlds.append(realm_world)

        return realm_worlds

    def create_world_backup(self, realm_guid: UUID4, world_name: str, backup_name: str):
        world_extensions = ["db", "fwl"]

        for extension in world_extensions:
            source_key = f"{realm_guid}/worlds/{world_name}/{world_name}.{extension}"
            destination_key = f"{realm_guid}/worlds/{backup_name}/{backup_name}.{extension}"

            try:
                self._s3.copy_object(
                    Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
                    CopySource={
                        'Bucket': settings.REALM_STORAGE_S3_BUCKET_NAME,
                        'Key': source_key
                    },
                    Key=destination_key
                )
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "")

                if error_code == 'NoSuchKey':
                    raise WorldNotFound(
                        msg=f"World '{world_name}' not found for realm '{realm_guid}'")
                else:
                    raise InvalidItemRequest(
                        msg="Failed to create world backup")

    def delete_world(self, realm_guid: UUID4, world_name: str):
        world_prefix = f"{realm_guid}/worlds/{world_name}/"

        response = self._s3.list_objects_v2(
            Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
            Prefix=world_prefix,
        )

        keys_to_delete = [{'Key': obj.get("Key", "")}
                          for obj in response.get('Contents', [])]

        if keys_to_delete:
            try:
                self._s3.delete_objects(
                    Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
                    Delete={
                        'Objects': keys_to_delete,  # type: ignore
                    }
                )
            except ClientError:
                raise InvalidItemRequest(msg="Failed to delete world")

    def get_realm_list_file(self, realm_guid: UUID4, file_name: str):
        file_key = f"{realm_guid}/lists/{file_name}"

        try:
            response = self._s3.get_object(
                Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
                Key=file_key
            )

            content = response.get("Body").read().decode('utf-8')

            realm_list_file = RealmListFile.model_validate({
                "file_name": file_name,
                "content": content
            })

            return realm_list_file
        except ClientError:
            raise RealmListFileNotFound(msg="Failed to get realm list file")

    def save_realm_list_file(self, realm_guid: UUID4, payload: CreateRealmFile):
        if payload.file_name not in ["permittedlist.txt", "bannedlist.txt", "adminlist.txt"]:
            raise InvalidRealmListFileName()

        file_key = f"{realm_guid}/lists/{payload.file_name}"

        try:
            self._s3.put_object(
                Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
                Key=file_key,
                Body=payload.content.encode('utf-8'),
                ContentType='text/plain'
            )
        except ClientError:
            raise InvalidItemRequest(msg="Failed to save realm list file")

    def open_portal(self, realm_guid: UUID4, user_guid: UUID4, payload: CreateRealmPortal):
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
            "password": payload.password,
            "preset": payload.preset,
            "modifiers": [modifier.model_dump() for modifier in payload.modifiers] if payload.modifiers else None,
            "keys": payload.keys,
            "modpack": payload.modpack,
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
