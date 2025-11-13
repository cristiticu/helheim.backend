from boto3.dynamodb.conditions import Key
from pydantic import UUID4
import settings
from shared.dynamodb import dynamodb_table
from accounts.exceptions import AccountNotFound
from accounts.model import Account


class AccountsPersistence():
    def __init__(self):
        self.accounts = dynamodb_table(settings.AUTH_TABLE_NAME)

    def persist(self, payload: Account):
        self.accounts.put_item(Item=payload.to_db_item())

    def get(self, guid: UUID4):
        response = self.accounts.get_item(Key={"guid": str(guid)})
        item = response.get("Item")

        if item is None:
            raise AccountNotFound()

        return Account.from_db_item(item)

    def get_by_username(self, username: str):
        response = self.accounts.query(KeyConditionExpression=Key(
            "username").eq(username), IndexName=settings.AUTH_TABLE_USERNAME_GSI)
        items = response.get("Items")

        if len(items) == 0:
            raise AccountNotFound()

        return Account.from_db_item(items[0])

    def delete(self, guid: UUID4):
        self.accounts.delete_item(Key={"guid": str(guid)})
