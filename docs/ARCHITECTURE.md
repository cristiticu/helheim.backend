# Architecture Overview

Helheim Backend is designed to operate as a serverless application on AWS, using FastAPI for web routing and Mangum as the ASGI adapter for AWS Lambda.

## Core Flow

1.  **Request Lifecycle**:
    -   Requests enter via AWS API Gateway.
    -   API Gateway invokes the Lambda function.
    -   **Mangum** acts as the bridge between the Lambda event and the **FastAPI** application.
    -   FastAPI routes the request based on the path and method.
    -   The response is then converted back by Mangum into a format API Gateway understands.

2.  **Application Structure**:
    -   `src/main.py`: The entry point for both local development and Lambda execution.
    -   `src/context.py`: Application context and shared states.
    -   `src/settings.py`: Configuration management via environment variables.

## Infrastructure Dependencies

### AWS Lambda
The service runs in a serverless environment, optimized for scalability and cost-efficiency. It uses Mangum with `lifespan="off"` to minimize cold start latency.

### DynamoDB
All persistent data (Accounts, Realms) is stored in DynamoDB tables. The application uses a single-table-like pattern for specific modules, though it maintains separate persistent layers for `accounts` and `realms`.

### S3
Used for storing world files for game servers. The `WorldManager` interacts with S3 to list, backup, and delete world data for Valheim and Vintage Story.

### EC2
The backend orchestrates game server instances. It interacts with EC2 to start, stop, and manage the lifecycle of the actual server nodes.

## Scalability and Performance
-   **Serverless**: Scaling is handled by AWS Lambda.
-   **FastAPI**: Provides high performance for I/O-bound tasks due to its asynchronous nature.
-   **Botocore/Boto3**: Used for efficient communication with AWS services.
