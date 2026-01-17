import boto3

from shared.utils import get_aws_env_params


def dynamodb_table(table_name: str):
    params = get_aws_env_params()

    dynamodb = boto3.resource(
        'dynamodb',
        **params
    )

    return dynamodb.Table(table_name)
