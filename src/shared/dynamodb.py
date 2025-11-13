import boto3


def dynamodb_table(table_name: str):
    dynamodb = boto3.resource(
        'dynamodb')
    return dynamodb.Table(table_name)
