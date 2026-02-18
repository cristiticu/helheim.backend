import uuid
from datetime import datetime, timezone

import pytest
from pwdlib import PasswordHash
import settings


pwd_context = PasswordHash.recommended()


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
    """Seed a test account with a hashed password."""
    guid = str(uuid.uuid4())
    username = "authuser"
    password_plain = "StrongPass123"
    password_hash = pwd_context.hash(password_plain)
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    accounts_table.put_item(
        Item={
            "guid": guid,
            "username": username,
            "password": password_hash,
            "c_at": c_at,
        }
    )

    return {"guid": guid, "username": username, "password": password_plain, "c_at": c_at}


@pytest.fixture
def refresh_auth_header(seeded_account):
    """Provide an Authorization header with a refresh JWT for the seeded user."""
    from auth.utils import create_access_token

    token = create_access_token(
        {"user_guid": seeded_account["guid"]}, expire=5)
    return {"Authorization": f"Bearer {token}"}
