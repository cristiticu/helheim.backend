from boto3.dynamodb.conditions import Key
from pydantic import UUID4
from exceptions import InvalidItemRequest
import settings
from botocore.exceptions import ClientError
from realms.exceptions import RealmListFileNotFound, RealmNotFound, RealmUserNotFound, WorldNotFound
from realms.model import Realm, RealmListFile, RealmPortal, RealmUser, RealmWorld
from shared.s3 import s3_client
from shared.dynamodb import dynamodb_table
from realms.world_manager import WorldManager


class RealmsPersistence():
    def __init__(self):
        self._realms = dynamodb_table(settings.REALMS_TABLE_NAME)
        self._realms_data_s3 = s3_client()
        self._world_manager = WorldManager(
            self._realms_data_s3, settings.REALM_STORAGE_S3_BUCKET_NAME)

    def persist_world_backup(self, realm_guid: UUID4, world_name: str, backup_name: str):
        realm = self.get_realm(realm_guid)
        try:
            self._world_manager.backup_world(realm, world_name, backup_name)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == 'NoSuchKey':
                raise WorldNotFound(
                    msg=f"World '{world_name}' not found for realm '{realm_guid}'")
            else:
                raise InvalidItemRequest(msg="Failed to create world backup")

    def persist_realm_list_file(self, realm_guid: UUID4, payload):
        file_key = f"{realm_guid}/lists/{payload.file_name}"

        try:
            self._realms_data_s3.put_object(
                Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
                Key=file_key,
                Body=payload.content.encode('utf-8'),
                ContentType='text/plain'
            )
        except ClientError:
            raise InvalidItemRequest(msg="Failed to save realm list file")

    def persist(self, payload: Realm | RealmPortal | RealmUser):
        self._realms.put_item(Item=payload.to_db_item())

    def get_realm(self, guid: UUID4) -> Realm:
        response = self._realms.get_item(
            Key={"guid": str(guid), "s_key": "REALM#DETAILS"})
        item = response.get("Item")

        if item is None:
            raise RealmNotFound()

        return Realm.from_db_item(item)

    def get_realms_for_user(self, user_guid: UUID4) -> list[RealmUser]:
        response = self._realms.query(
            KeyConditionExpression=Key("user_guid").eq(str(user_guid)),
            IndexName=settings.REALMS_TABLE_USER_GUID_GSI,
        )
        items = response.get("Items", [])

        return [RealmUser.from_db_item(item) for item in items]

    def get_realm_user(self, realm_guid: UUID4, user_guid: UUID4) -> RealmUser:
        response = self._realms.get_item(
            Key={"guid": str(realm_guid), "s_key": f"USER#{user_guid}"}
        )
        item = response.get("Item")

        if item is None:
            raise RealmUserNotFound()

        return RealmUser.from_db_item(item)

    def get_realm_users(self, guid: UUID4) -> list[RealmUser]:
        response = self._realms.query(
            KeyConditionExpression=Key("guid").eq(
                str(guid)) & Key("s_key").begins_with("USER#"),
        )
        items = response.get("Items", [])

        return [RealmUser.from_db_item(item) for item in items]

    def get_realm_portals(self, guid: UUID4) -> list[RealmPortal]:
        response = self._realms.query(
            KeyConditionExpression=Key("guid").eq(
                str(guid)) & Key("s_key").begins_with("PORTAL#"),
        )
        items = response.get("Items", [])

        return [RealmPortal.from_db_item(item) for item in items]

    def delete_portal(self, realm_guid: UUID4, portal_guid: UUID4):
        self._realms.delete_item(
            Key={"guid": str(realm_guid), "s_key": f"PORTAL#{portal_guid}"}
        )

    def get_realm_worlds(self, guid: UUID4) -> list[RealmWorld]:
        realm = self.get_realm(guid)
        return self._world_manager.get_worlds(realm)

    def delete_world(self, realm_guid: UUID4, world_name: str):
        realm = self.get_realm(realm_guid)
        try:
            self._world_manager.delete_world(realm, world_name)
        except ClientError:
            raise InvalidItemRequest(msg="Failed to delete world")

    def get_realm_list_file(self, realm_guid: UUID4, file_name: str):
        file_key = f"{realm_guid}/lists/{file_name}"

        try:
            response = self._realms_data_s3.get_object(
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
