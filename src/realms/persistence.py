from boto3.dynamodb.conditions import Key
from pydantic import UUID4
from exceptions import InvalidItemRequest
import settings
from botocore.exceptions import ClientError
from realms.exceptions import RealmListFileNotFound, RealmNotFound, RealmUserNotFound, WorldNotFound
from realms.model import Realm, RealmListFile, RealmPortal, RealmUser, RealmWorld
from shared.s3 import s3_client
from shared.dynamodb import dynamodb_table


class RealmsPersistence():
    def __init__(self):
        self._realms = dynamodb_table(settings.REALMS_TABLE_NAME)
        self._realms_data_s3 = s3_client()

    def persist_world_backup(self, realm_guid: UUID4, world_name: str, backup_name: str):
        world_extensions = ["db", "fwl"]

        for extension in world_extensions:
            source_key = f"{realm_guid}/worlds/{world_name}/{world_name}.{extension}"
            destination_key = f"{realm_guid}/worlds/{backup_name}/{backup_name}.{extension}"

            try:
                self._realms_data_s3.copy_object(
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
        search_prefix = f"{guid}/worlds/"
        delimiter = "/"

        world_names = []

        response = self._realms_data_s3.list_objects_v2(
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

            response = self._realms_data_s3.head_object(
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

    def delete_world(self, realm_guid: UUID4, world_name: str):
        world_prefix = f"{realm_guid}/worlds/{world_name}/"

        response = self._realms_data_s3.list_objects_v2(
            Bucket=settings.REALM_STORAGE_S3_BUCKET_NAME,
            Prefix=world_prefix,
        )

        keys_to_delete = [{'Key': obj.get("Key", "")}
                          for obj in response.get('Contents', [])]

        if keys_to_delete:
            try:
                self._realms_data_s3.delete_objects(
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
