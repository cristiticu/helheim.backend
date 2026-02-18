import uuid
from datetime import datetime, timezone

import pytest
import settings


@pytest.fixture
def realms_table(dynamodb_resource):
    """Create the realms DynamoDB table with required schema and GSI (moto)."""
    dynamodb_resource.create_table(
        TableName=settings.REALMS_TABLE_NAME,
        AttributeDefinitions=[
            {"AttributeName": "guid", "AttributeType": "S"},
            {"AttributeName": "s_key", "AttributeType": "S"},
            {"AttributeName": "user_guid", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "guid", "KeyType": "HASH"},
            {"AttributeName": "s_key", "KeyType": "RANGE"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": settings.REALMS_TABLE_USER_GUID_GSI,
                "KeySchema": [
                    {"AttributeName": "user_guid", "KeyType": "HASH"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    table = dynamodb_resource.Table(settings.REALMS_TABLE_NAME)
    yield table


@pytest.fixture
def realms_bucket(s3_client):
    """Ensure S3 bucket for realms exists."""
    bucket = settings.REALM_STORAGE_S3_BUCKET_NAME
    # us-east-1 does not require LocationConstraint
    s3_client.create_bucket(Bucket=bucket)
    return bucket


@pytest.fixture
def realm_guid():
    return str(uuid.uuid4())


@pytest.fixture
def user_guid():
    return str(uuid.uuid4())


@pytest.fixture
def auth_header(user_guid):
    from auth.utils import create_access_token
    token = create_access_token({"user_guid": user_guid}, expire=60)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def seeded_realm(realms_table, realm_guid):
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    item = {
        "guid": realm_guid,
        "s_key": "REALM#DETAILS",
        "name": "My Realm",
        "description": "Test realm",
        "c_at": c_at,
        "realm_type": "valheim",
        "meta_type": "REALM",
    }
    realms_table.put_item(Item=item)
    return item


@pytest.fixture
def seeded_realm_vintage(realms_table, realm_guid):
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    item = {
        "guid": realm_guid,
        "s_key": "REALM#DETAILS",
        "name": "Vintage Realm",
        "description": "Vintage story realm",
        "c_at": c_at,
        "realm_type": "vintage_story",
        "meta_type": "REALM",
    }
    realms_table.put_item(Item=item)
    return item


@pytest.fixture
def seeded_realm_user_admin(realms_table, realm_guid, user_guid):
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    item = {
        "guid": realm_guid,
        "s_key": f"USER#{user_guid}",
        "username": "realmuser",
        "user_guid": user_guid,
        "role": "admin",
        "c_at": c_at,
        "meta_type": "REALM_USER",
    }
    realms_table.put_item(Item=item)
    return item


@pytest.fixture
def seeded_realm_user_member(realms_table, realm_guid, user_guid):
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    item = {
        "guid": realm_guid,
        "s_key": f"USER#{user_guid}",
        "username": "realmuser",
        "user_guid": user_guid,
        "role": "member",
        "c_at": c_at,
        "meta_type": "REALM_USER",
    }
    realms_table.put_item(Item=item)
    return item


@pytest.fixture
def seeded_world_valheim(s3_client, realms_bucket, realm_guid):
    world_name = "Midgard"
    base = f"{realm_guid}/worlds/{world_name}"
    s3_client.put_object(Bucket=realms_bucket,
                         Key=f"{base}/{world_name}.db", Body=b"db")
    s3_client.put_object(Bucket=realms_bucket,
                         Key=f"{base}/{world_name}.fwl", Body=b"fwl")
    return world_name


@pytest.fixture
def seeded_world_vintage(s3_client, realms_bucket, realm_guid):
    world_name = "Antique"
    base = f"{realm_guid}/worlds/{world_name}"
    s3_client.put_object(Bucket=realms_bucket,
                         Key=f"{base}/default.vcdbs", Body=b"vcdbs")
    return world_name


@pytest.fixture
def seeded_portal(realms_table, realm_guid):
    c_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    portal_guid = str(uuid.uuid4())
    item = {
        "guid": realm_guid,
        "s_key": f"PORTAL#{portal_guid}",
        "opened_by_user_guid": str(uuid.uuid4()),
        "instance_id": "i-abc123",
        "spot_request_id": "sir-abc123",
        "name": "ServerName",
        "world_name": "World",
        "password": "secretpw",
        "public_address": "1.2.3.4",
        "region": "us-east-1",
        "instance_type": "t3.small",
        "status": "running",
        "c_at": c_at,
        "meta_type": "REALM_PORTAL",
    }
    realms_table.put_item(Item=item)
    return item


@pytest.fixture
def seeded_list_file_adminlist(s3_client, realms_bucket, realm_guid):
    key = f"{realm_guid}/lists/adminlist.txt"
    s3_client.put_object(Bucket=realms_bucket, Key=key, Body=b"admin1\nadmin2")
    return {"file_name": "adminlist.txt", "content": "admin1\nadmin2"}


@pytest.fixture
def stub_lambda_invocation(monkeypatch):
    from realms.service import RealmsService

    def _valheim(_self, realm, payload):
        return {
            "instanceId": "i-123",
            "spotRequestId": "sir-123",
            "config": {"serverName": payload.name, "worldName": payload.world_name},
            "publicIpAddress": "5.6.7.8",
            "region": "us-east-1",
            "instanceType": "t3.small",
            "status": "running",
        }

    def _vintage(_self, realm, payload):
        return {
            "instanceId": "i-456",
            "spotRequestId": "sir-456",
            "config": {"serverName": payload.name, "worldName": payload.world_name},
            "publicIpAddress": "9.10.11.12",
            "region": "us-east-1",
            "instanceType": "t3.micro",
            "status": "running",
        }

    monkeypatch.setattr(
        RealmsService, "invoke_valheim_instance_lambda", _valheim)
    monkeypatch.setattr(
        RealmsService, "invoke_vintage_story_instance_lambda", _vintage)
    return True
