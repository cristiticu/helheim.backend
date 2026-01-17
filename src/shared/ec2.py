import boto3
import settings


def ec2_client():
    return boto3.client('ec2',
                        region_name=settings.AWS_REGION_NAME,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        endpoint_url=settings.AWS_ENDPOINT_URL
                        )
