# Shared Utilities Module

The `shared` module contains utility functions, standardized AWS clients, and helper classes used across all modules.

## 🧱 Components

### 1. `dynamodb.py`
A wrapper around the **Boto3** `Table` resource.
- **`dynamodb_table(table_name: str)`**: Returns a thread-safe DynamoDB `Table` instance.
- **Purpose**: Provides a consistent way to obtain the DynamoDB client with proper configuration (endpoints, region, etc.).

### 2. `s3.py`
A wrapper around the **Boto3** `S3` client.
- **`s_3_client()`**: Returns an S3 client configured with the appropriate AWS credentials and endpoints from `settings.py`.

### 3. `ec2.py`
(If present) Utility for low-level EC2 operations.

### 4. `lambda_client.py`
A wrapper around the **Boto3** `Lambda` client.
- **`lambda_client()`**: Used to invoke the instance management Lambdas.

### 5. `utils.py`
General-purpose helper functions.
- **`format_utc_datetime_string(dt: datetime)`**: Standardizes how timestamps are stored in DynamoDB (ISO 8601 format).
- **`parse_utc_datetime_string(dt_str: str)`**: Converts ISO 8601 strings back into Pydantic-compatible `datetime` objects.
- **GUID generation**: Helpers for creating and validating UUIDv4 strings.

## 🛠 Patterns and Specifics

- **Client Caching**: Boto3 clients should be reused where possible within a request context to avoid the overhead of multiple client initializations.
- **Standardized Datetime**: All timestamps in the Helheim system must be in UTC. The `shared.utils` module provides the standard conversion logic to maintain consistency.
- **S3 Key Generation**: Standardized patterns for building S3 object keys (e.g., `{realm_guid}/...`) are partially managed here and in `realms.world_manager`.
- **Environment Awareness**: All AWS clients in this module respect the `AWS_ENDPOINT_URL` setting, allowing for easy switching between LocalStack (local) and real AWS (production).
