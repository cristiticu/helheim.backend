# Shared Module

The **Shared** module contains reusable components and AWS SDK wrappers used across the Helheim Backend.

## Components

### `src/shared/dynamodb.py`
Provides a wrapper for DynamoDB client operations:
-   `get_dynamodb_client`: Returns a configured `boto3.client` for DynamoDB.
-   `create_table`: Used for local database initialization.
-   `delete_table`: Used for clearing local test tables.

### `src/shared/s3.py`
Contains the `S3Client` wrapper and related utilities for interacting with Amazon S3. It provides functions for:
-   `get_s3_client`: Returns a configured `boto3.client` for S3.
-   `upload_file`, `download_file`: Core file operations.
-   `list_objects`: Searching for files within S3 buckets.

### `src/shared/ec2.py`
Provides an `EC2Client` wrapper for interacting with Amazon EC2 instances:
-   `get_ec2_client`: Returns a configured `boto3.client` for EC2.
-   `start_instance`, `stop_instance`: Lifecycle management functions.
-   `get_instance_status`: Retrieves the current state of a game server instance.

### `src/shared/lambda_client.py`
A wrapper for invoking other AWS Lambda functions or managing its own Lambda-related configurations.
-   `get_lambda_client`: Returns a configured `boto3.client` for Lambda.

### `src/shared/utils.py`
General-purpose utility functions:
-   `get_logger`: A standard logger configuration for consistent output across all modules.
-   `generate_guid`: Helper for generating UUIDs.
-   `parse_env_var`: Utility for reading and parsing environment variables.

### `src/shared/__init__.py`
Exports key classes and functions for easy access from other modules.

## Design Philosophy

The `shared` module is designed to:
1.  **Reduce Code Duplication**: Standardizes how AWS services are accessed.
2.  **Simplify Mocking**: Centralizes AWS client creation, making it easier to replace with `moto` in tests.
3.  **Provide Consistent Logging**: Ensures all modules use the same logging format and levels.
