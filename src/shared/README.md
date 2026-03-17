# Shared Module

The `shared` module contains common utilities, AWS client wrappers, and infrastructure-related helper functions used across all Helheim domain modules.

## Responsibilities

- **AWS Client Initialization:** Unified factory methods for Boto3 clients (`DynamoDB`, `S3`, `EC2`, `Lambda`).
- **Data Persistence Helpers:** Low-level DynamoDB operations and data transformation utilities.
- **Resource Management:** Interfaces for basic AWS resource interactions (e.g., S3 buckets, EC2 instance metadata).
- **Utility Functions:** Global helper functions like timestamp formatting or unique identifier generation.

## Core Components

- `dynamodb.py`: Helper class/functions for standard DynamoDB CRUD operations.
- `ec2.py`: Unified interface for initializing and interacting with AWS EC2 service.
- `lambda_client.py`: Unified interface for initializing and interacting with AWS Lambda service.
- `s3.py`: Unified interface for initializing and interacting with AWS S3 service.
- `utils.py`: Generic utility functions used throughout the backend.
