# Testing Guide

The Helheim Backend testing suite uses **pytest** and **moto** to ensure reliability and correct behavior across its modules.

## Tooling

-   **pytest**: The core testing framework.
-   **moto**: A library for mocking AWS services (DynamoDB, S3, EC2).
-   **httpx**: Used for testing FastAPI endpoints via its `TestClient`.

## Structure

Tests are located in the `tests/` directory, mirroring the structure of `src/`.

-   `tests/auth/`: Tests for authentication and token logic.
-   `tests/accounts/`: Tests for account management and persistence.
-   `tests/realms/`: Tests for realm orchestration and world management.
-   `tests/conftest.py`: Root-level fixtures and global configuration.

### Module-specific Conftest
Each module has its own `conftest.py` (e.g., `tests/auth/conftest.py`) containing:
-   Fixtures for specific services (`auth_service`, `account_service`, `realm_service`).
-   Mocked persistence layers (`account_persistence`, `realm_persistence`).
-   AWS client mocks using moto.

## Mocking Strategy

The test suite relies heavily on mocking to provide a consistent and isolated testing environment.

1.  **AWS Services**: `moto` decorators (`@mock_dynamodb`, `@mock_s3`, `@mock_ec2`) are used in fixtures to simulate AWS infrastructure without making real network calls or requiring credentials.
2.  **Service Layers**: Business logic services are often tested with mocked persistence layers to verify logic independently of the database.
3.  **API Endpoints**: `TestClient` is used to send HTTP requests to the FastAPI application, ensuring routers and middleware are correctly configured.

## Running Tests

To run the full test suite:
```bash
pytest
```

To run tests for a specific module:
```bash
pytest tests/auth
```

To run with coverage (if configured):
```bash
pytest --cov=src
```

## Configuration

Test-specific configuration is handled in `pytest.toml` at the project root. This file defines:
-   Test paths.
-   Log levels.
-   Environment variables for tests.
-   Marker definitions.
