import boto3
import settings


def ec2_client():
    return boto3.client('ec2', region_name=settings.AWS_REGION_NAME)
