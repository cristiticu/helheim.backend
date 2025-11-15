import boto3
import settings


def s3_client():
    return boto3.client('s3', region_name=settings.AWS_REGION_NAME)
