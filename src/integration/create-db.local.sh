#!/usr/bin/env bash
set -euo pipefail

aws dynamodb create-table   --profile localstack \
                            --table-name "helheim.table.authentication" \
                            --attribute-definitions '[{"AttributeName":"guid","AttributeType":"S"},{"AttributeName":"username","AttributeType":"S"}]' \
                            --key-schema "AttributeName=guid,KeyType=HASH" \
                            --global-secondary-indexes "IndexName=gsi.username,KeySchema=[{AttributeName=username,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
                                                        --billing-mode PAY_PER_REQUEST

aws dynamodb create-table   --profile localstack \
                            --table-name "helheim.table.realms" \
                            --attribute-definitions '[{"AttributeName":"guid","AttributeType":"S"},{"AttributeName":"s_key","AttributeType":"S"},{"AttributeName":"user_guid","AttributeType":"S"}]' \
                            --key-schema '[{"AttributeName":"guid","KeyType":"HASH"},{"AttributeName":"s_key","KeyType":"RANGE"}]' \
                            --global-secondary-indexes "IndexName=gsi.user-realms-lookup-2,KeySchema=[{AttributeName=user_guid,KeyType=HASH},{AttributeName=guid,KeyType=RANGE}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
                                                        --billing-mode PAY_PER_REQUEST

aws s3 mb s3://helheim.storage --profile localstack

# Wait for tables to exist (helps on fresh localstack startups)
aws dynamodb wait table-exists --profile localstack --table-name "helheim.table.authentication"
aws dynamodb wait table-exists --profile localstack --table-name "helheim.table.realms"

# Seed data: one auth user and two realms (valheim, vintage_story)
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
USER_GUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
REALM1_GUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
REALM2_GUID=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Insert demo user into authentication table (respects Account model)
aws dynamodb put-item --profile localstack \
    --table-name "helheim.table.authentication" \
    --item '{
        "guid": {"S": "'"$USER_GUID"'"},
        "username": {"S": "demo"},
        "password": {"S": "$argon2id$v=19$m=65536,t=3,p=4$taDJ/Hosg229sF72utkcwA$R4VoUM3An8LZCg5VPLD8yk8JTSUNBGRK3EIk4EBQE3g"},
        "c_at": {"S": "'"$NOW"'"}
    }'

# Insert two realm records (respects Realm model)
aws dynamodb put-item --profile localstack \
    --table-name "helheim.table.realms" \
    --item '{
        "guid": {"S": "'"$REALM1_GUID"'"},
        "s_key": {"S": "REALM#DETAILS"},
        "name": {"S": "Valheim Realm"},
        "description": {"S": "Seed realm for Valheim"},
        "c_at": {"S": "'"$NOW"'"},
        "realm_type": {"S": "valheim"},
        "meta_type": {"S": "REALM"}
    }'

aws dynamodb put-item --profile localstack \
    --table-name "helheim.table.realms" \
    --item '{
        "guid": {"S": "'"$REALM2_GUID"'"},
        "s_key": {"S": "REALM#DETAILS"},
        "name": {"S": "Vintage Story Realm"},
        "description": {"S": "Seed realm for Vintage Story"},
        "c_at": {"S": "'"$NOW"'"},
        "realm_type": {"S": "vintage_story"},
        "meta_type": {"S": "REALM"}
    }'

# Link demo user to both realms (RealmUser items)
aws dynamodb put-item --profile localstack \
    --table-name "helheim.table.realms" \
    --item '{
        "guid": {"S": "'"$REALM1_GUID"'"},
        "s_key": {"S": "USER#'"$USER_GUID"'"},
        "username": {"S": "demo"},
        "user_guid": {"S": "'"$USER_GUID"'"},
        "role": {"S": "OWNER"},
        "c_at": {"S": "'"$NOW"'"},
        "meta_type": {"S": "REALM_USER"}
    }'

aws dynamodb put-item --profile localstack \
    --table-name "helheim.table.realms" \
    --item '{
        "guid": {"S": "'"$REALM2_GUID"'"},
        "s_key": {"S": "USER#'"$USER_GUID"'"},
        "username": {"S": "demo"},
        "user_guid": {"S": "'"$USER_GUID"'"},
        "role": {"S": "OWNER"},
        "c_at": {"S": "'"$NOW"'"},
        "meta_type": {"S": "REALM_USER"}
    }'
