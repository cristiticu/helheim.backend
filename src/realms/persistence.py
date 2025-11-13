from boto3.dynamodb.conditions import Key
from httpx import delete
from pydantic import UUID4
import settings
from realms.exceptions import RealmNotFound
from realms.model import Realm, RealmPortal, RealmUser
from shared.dynamodb import dynamodb_table


class RealmsPersistence():
    def __init__(self):
        self.realms = dynamodb_table(settings.REALMS_TABLE_NAME)

    def persist(self, payload: Realm | RealmPortal | RealmUser):
        self.realms.put_item(Item=payload.to_db_item())

    def get_realm(self, guid: UUID4) -> Realm:
        response = self.realms.get_item(
            Key={"guid": str(guid), "s_key": "REALM#DETAILS"})
        item = response.get("Item")

        if item is None:
            raise RealmNotFound()

        return Realm.from_db_item(item)

    def get_realms_for_user(self, user_guid: UUID4) -> list[RealmUser]:
        response = self.realms.query(
            KeyConditionExpression=Key("user_guid").eq(str(user_guid)),
            IndexName=settings.REALMS_TABLE_USER_GUID_GSI,
        )
        items = response.get("Items", [])

        return [RealmUser.from_db_item(item) for item in items]

    def get_realm_users(self, guid: UUID4) -> list[RealmUser]:
        response = self.realms.query(
            KeyConditionExpression=Key("guid").eq(
                str(guid)) & Key("s_key").begins_with("USER#"),
        )
        items = response.get("Items", [])

        return [RealmUser.from_db_item(item) for item in items]

    def get_realm_portals(self, guid: UUID4) -> list[RealmPortal]:
        response = self.realms.query(
            KeyConditionExpression=Key("guid").eq(
                str(guid)) & Key("s_key").begins_with("PORTAL#"),
        )
        items = response.get("Items", [])

        return [RealmPortal.from_db_item(item) for item in items]

    def delete_portal(self, realm_guid: UUID4, portal_guid: UUID4):
        self.realms.delete_item(
            Key={"guid": str(realm_guid), "s_key": f"PORTAL#{portal_guid}"}
        )
