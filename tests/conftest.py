import boto3
import pytest
from moto import mock_aws
from fastapi.testclient import TestClient


@pytest.fixture()
def mocked_aws():
    """Global mock for all AWS services during the test."""
    with mock_aws():
        yield


@pytest.fixture
def dynamodb_resource(mocked_aws):
    """Provides a mocked DynamoDB client."""
    return boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture
def s3_client(mocked_aws):
    """Provides a mocked S3 client."""
    return boto3.client("s3", region_name="us-east-1")


@pytest.fixture
def ec2_client(mocked_aws):
    """Provides a mocked EC2 client."""
    return boto3.client("ec2", region_name="us-east-1")


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient."""
    from main import app

    with TestClient(app) as client:
        yield client
