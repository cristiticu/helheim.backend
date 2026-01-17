import boto3
from shared.utils import get_aws_env_params


def lambda_client():
    params = get_aws_env_params()

    return boto3.client("lambda",
                        **params
                        )
