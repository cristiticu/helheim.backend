import boto3
import settings


def lambda_client():
    return boto3.client("lambda", region_name=settings.AWS_REGION_NAME)
