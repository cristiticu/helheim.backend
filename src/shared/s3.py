import boto3
from shared.utils import get_aws_env_params


def s3_client():
    params = get_aws_env_params()

    return boto3.client(
        's3',
        **params
    )


def s3_bucket(bucket_name: str):
    params = get_aws_env_params()

    s3 = boto3.resource(
        's3',
        **params
    )

    return s3.Bucket(bucket_name)
