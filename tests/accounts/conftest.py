import uuid
from datetime import datetime, timezone
import pytest
from auth.utils import create_access_token
import settings


@pytest.fixture
def accounts_table(dynamodb_resource):
    """Create the accounts DynamoDB table with required schema (moto)."""

    dynamodb_resource.create_table(
        TableName=settings.AUTH_TABLE_NAME,
        AttributeDefinitions=[
            {"AttributeName": "guid", "AttributeType": "S"},
            {"AttributeName": "username", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "guid", "KeyType": "HASH"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": settings.AUTH_TABLE_USERNAME_GSI,
                "KeySchema": [
                    {"AttributeName": "username", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    table = dynamodb_resource.Table(settings.AUTH_TABLE_NAME)
    yield table


@pytest.fixture
def seeded_account(accounts_table):
    """Seed a test account item into the table and return its data."""
    guid = str(uuid.uuid4())
    username = "testuser"
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    accounts_table.put_item(
        Item={
            "guid": guid,
            "username": username,
            "password": "hashed-password-placeholder",
            "c_at": c_at,
        }
    )

    return {"guid": guid, "username": username, "c_at": c_at}


@pytest.fixture
def auth_header():
    """Provide an Authorization header with a valid JWT for tests."""
    token = create_access_token({"user_guid": str(uuid.uuid4())}, expire=5)
    return {"Authorization": f"Bearer {token}"}
