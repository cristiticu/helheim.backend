# Shared Module

## Purpose
The `shared` module contains common utilities, AWS clients, and foundational code shared across all other modules in the application.

## Structure
- `dynamodb.py`: Utility functions for interacting with DynamoDB.
- `s3.py`: Utility functions for interacting with S3.
- `ec2.py`: Utility functions for interacting with EC2 (if used).
- `lambda_client.py`: Utility functions for interacting with AWS Lambda.
- `utils.py`: Common helper functions (e.g., password hashing, date/time formatting).
- `__init__.py`: Exports common utilities.

## Design Patterns

### Client Singleton Pattern
AWS clients (boto3) are initialized and shared through utility functions (e.g., `dynamodb_table`, `s3_client`). This pattern ensures efficient connection management and simplifies client configuration.

### Common Utilities
Common helper functions are isolated in this module to avoid code duplication and ensure consistency across the application. This includes shared logic for password hashing (via `pwdlib`) and time-related operations.
