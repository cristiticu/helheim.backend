# Helheim Backend

Helheim Backend is a FastAPI-based service designed to manage game server realms, accounts, and authentication. It is architected to run as a serverless application on AWS Lambda using Mangum, while also supporting local development.

## Core Features

- **Authentication**: JWT-based authentication system.
- **Account Management**: User profile and preference management.
- **Realm Management**: Orchestration of game servers (Valheim, Vintage Story).
- **World Management**: S3-based world file handling (backups, deletions, listings).
- **Infrastructure**: Tight integration with AWS (DynamoDB, S3, EC2, Lambda).

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - Deep dive into the AWS and FastAPI flow.
- [API Design](docs/API_DESIGN.md) - Routing, Dependency Injection, and Exception handling.
- [Testing Guide](docs/TESTING.md) - Overview of the test suite using pytest and moto.

## Modules

- [Accounts](src/accounts/README.md) - User account persistence and logic.
- [Auth](src/auth/README.md) - Security and token management.
- [Realms](src/realms/README.md) - Game server orchestration and world management.
- [Shared](src/shared/README.md) - AWS SDK wrappers and utility functions.
- [Routers](src/routers/README.md) - API endpoint definitions.
- [Integration](src/integration/README.md) - Database initialization and local setup.

## Getting Started

### Local Development

1. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

2. Start the local environment:
   ```bash
   ./run.local.sh
   ```

3. Initialize the local database (requires Docker/LocalStack or a running DynamoDB instance):
   ```bash
   ./src/integration/create-db.local.sh
   ```

## Deployment

The application is deployed as an AWS Lambda function. The entry point is `src/main.py`, where the FastAPI app is wrapped by Mangum for Lambda compatibility.
