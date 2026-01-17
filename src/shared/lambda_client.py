import boto3
import settings


def lambda_client():
    return boto3.client("lambda",
                        region_name=settings.AWS_REGION_NAME,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        endpoint_url=settings.AWS_ENDPOINT_URL
                        )
