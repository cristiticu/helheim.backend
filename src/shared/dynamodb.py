import boto3
import settings


def dynamodb_table(table_name: str):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_ENDPOINT_URL
    )

    return dynamodb.Table(table_name)
