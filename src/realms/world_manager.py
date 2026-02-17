from botocore.exceptions import ClientError
from pydantic import UUID4
from realms.exceptions import WorldNotFound
from realms.model import Realm, RealmWorld


class WorldManager:
    def __init__(self, s3_client, bucket_name: str):
        self._s3 = s3_client
        self._bucket = bucket_name

    def get_worlds(self, realm: Realm) -> list[RealmWorld]:
        world_type = self._get_world_type(realm)
        guid = realm.guid
        search_prefix = f"{guid}/worlds/"
        delimiter = "/"

        world_names: list[str] = []

        response = self._s3.list_objects_v2(
            Bucket=self._bucket,
            Prefix=search_prefix,
            Delimiter=delimiter,
        )

        for prefix in response.get("CommonPrefixes", []):
            full_prefix = prefix.get("Prefix", "")
            world_name = full_prefix.replace(
                search_prefix, "").rstrip(delimiter)
            if world_name:
                world_names.append(world_name)

        realm_worlds: list[RealmWorld] = []

        for world_name in world_names:
            last_modified = self._get_world_last_modified(
                guid, world_name, world_type)
            if last_modified is None:
                # Skip folders without recognizable world files
                continue

            realm_world_payload = {
                "name": world_name,
                "m_at": last_modified,
            }
            realm_world = RealmWorld.model_validate(realm_world_payload)
            realm_worlds.append(realm_world)

        return realm_worlds

    def backup_world(self, realm: Realm, world_name: str, backup_name: str):
        world_type = self._get_world_type(realm)
        guid = realm.guid

        if world_type == "vintage_story":
            # Vintage Story: single .vcdbs file
            source_key = self._vcdbs_key(guid, world_name)
            if not self._object_exists(source_key):
                raise WorldNotFound(
                    msg=f"World '{world_name}' not found for realm '{guid}'")
            self._copy_object(
                source_key=source_key,
                destination_key=self._vcdbs_key(guid, backup_name),
            )
            return

        # Default: Valheim (.db + .fwl)
        valheim_keys = [
            self._db_key(guid, world_name),
            self._fwl_key(guid, world_name),
        ]

        if not all(self._object_exists(k) for k in valheim_keys):
            raise WorldNotFound(
                msg=f"World '{world_name}' not found for realm '{guid}'")

        self._copy_object(
            source_key=self._db_key(guid, world_name),
            destination_key=self._db_key(guid, backup_name),
        )
        self._copy_object(
            source_key=self._fwl_key(guid, world_name),
            destination_key=self._fwl_key(guid, backup_name),
        )

    def delete_world(self, realm: Realm, world_name: str):
        guid = realm.guid
        world_prefix = f"{guid}/worlds/{world_name}/"
        response = self._s3.list_objects_v2(
            Bucket=self._bucket,
            Prefix=world_prefix,
        )

        keys_to_delete = [{"Key": obj.get("Key", "")}
                          for obj in response.get("Contents", [])]

        if keys_to_delete:
            self._s3.delete_objects(
                Bucket=self._bucket,
                Delete={"Objects": keys_to_delete},  # type: ignore
            )

    # --- Helpers ---
    def _db_key(self, realm_guid: UUID4, world_name: str) -> str:
        return f"{realm_guid}/worlds/{world_name}/{world_name}.db"

    def _fwl_key(self, realm_guid: UUID4, world_name: str) -> str:
        return f"{realm_guid}/worlds/{world_name}/{world_name}.fwl"

    def _vcdbs_key(self, realm_guid: UUID4, world_name: str) -> str:
        return f"{realm_guid}/worlds/{world_name}/default.vcdbs"

    def _object_exists(self, key: str) -> bool:
        try:
            self._s3.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code in ("404", "NoSuchKey"):
                return False
            # For other errors, bubble up
            raise

    def _get_world_last_modified(self, realm_guid: UUID4, world_name: str, world_type: str):
        keys = (
            [self._vcdbs_key(realm_guid, world_name)]
            if world_type == "vintage_story"
            else [self._db_key(realm_guid, world_name)]
        )

        for key in keys:
            try:
                response = self._s3.head_object(Bucket=self._bucket, Key=key)
                return response.get("LastModified")
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "")
                if error_code in ("404", "NoSuchKey"):
                    continue
                raise
        return None

    def _get_world_type(self, realm: Realm) -> str:
        # Expect exact types: "valheim" or "vintage_story"
        return getattr(realm, "realm_type", "valheim")

    def _copy_object(self, source_key: str, destination_key: str):
        try:
            self._s3.copy_object(
                Bucket=self._bucket,
                CopySource={"Bucket": self._bucket, "Key": source_key},
                Key=destination_key,
            )
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code in ("404", "NoSuchKey"):
                raise WorldNotFound(msg="World source file not found")
            raise
