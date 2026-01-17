aws dynamodb create-table   --profile localstack \
                            --table-name "helheim.table.authentication" \
                            --attribute-definitions '[{"AttributeName":"guid","AttributeType":"S"},{"AttributeName":"username","AttributeType":"S"}]' \
                            --key-schema "AttributeName=guid,KeyType=HASH" \
                            --global-secondary-indexes "IndexName=gsi.username,KeySchema=[{AttributeName=username,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
                            --billing-mode PAY_PER_REQUEST \

aws dynamodb create-table   --profile localstack \
                            --table-name "helheim.table.realms" \
                            --attribute-definitions '[{"AttributeName":"guid","AttributeType":"S"},{"AttributeName":"s_key","AttributeType":"S"},{"AttributeName":"user_guid","AttributeType":"S"}]' \
                            --key-schema '[{"AttributeName":"guid","KeyType":"HASH"},{"AttributeName":"s_key","KeyType":"RANGE"}]' \
                            --global-secondary-indexes "IndexName=gsi.user-realms-lookup-2,KeySchema=[{AttributeName=user_guid,KeyType=HASH},{AttributeName=guid,KeyType=RANGE}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" \
                            --billing-mode PAY_PER_REQUEST \

aws s3 mb s3://helheim.storage --profile localstack
