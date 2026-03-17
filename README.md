# Helheim Backend

## Project Overview
Helheim Backend is a robust, scalable backend service designed for managing game realms, user accounts, and authentication. Built with **FastAPI** and designed for deployment on **AWS Lambda**, it leverages a modern serverless architecture to provide high availability and cost-efficiency.

## Architecture
The project follows a clean, layered architecture:

- **API Layer (FastAPI)**: Handles HTTP requests, validation, and routing.
- **Service Layer**: Contains business logic, orchestrating calls between the API and persistence layers.
- **Persistence Layer (Repository Pattern)**: Abstracts data access, interacting with DynamoDB and S3.
- **Deployment (AWS Lambda & Mangum)**: The FastAPI application is wrapped with Mangum for execution in AWS Lambda environments.

### Tech Stack
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Runtime**: Python 3.12+
- **Database**: [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) (Single-Table Design)
- **Storage**: [Amazon S3](https://aws.amazon.com/s3/)
- **Serverless Wrapper**: [Mangum](https://mangum.io/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Dependency Management**: [uv](https://github.com/astral-sh/uv)

## Project Structure
```text
src/
├── accounts/      # User account management
├── auth/          # Authentication and Authorization
├── realms/        # Game realm management
├── routers/       # FastAPI route definitions
├── shared/        # Shared utilities and AWS clients
├── main.py        # Application entry point & Lambda handler
└── settings.py    # Configuration management
tests/             # Comprehensive test suite
```

## Design Patterns

### Single-Table Design
We utilize Amazon DynamoDB with a Single-Table Design pattern. This allows us to store multiple entity types (Accounts, Realms, Users, Portals) in the same table, optimized for efficient querying using Partition Keys (PK) and Sort Keys (SK).

### Repository Pattern
Data access is encapsulated within `Persistence` classes (e.g., `AccountsPersistence`, `RealmsPersistence`). This decouples the business logic from the underlying database schema and AWS SDK (boto3) calls.

### Service Layer Separation
Business rules are isolated in `Service` classes (e.g., `AccountsService`). Routers depend on Services, and Services depend on Persistence classes, ensuring a clear unidirectional flow of dependency and making the code highly testable.

## Getting Started
### Prerequisites
- Python 3.12
- `uv` for package management
- AWS CLI configured (for cloud resources)

### Installation
```bash
uv sync
```

### Running Locally
```bash
./run.local.sh
```

### Running Tests
```bash
uv run pytest
```
