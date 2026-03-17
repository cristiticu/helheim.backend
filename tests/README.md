# Tests Module

## Purpose
The `tests` module contains a comprehensive suite of unit and integration tests to ensure code quality and maintainability.

## Structure
- `accounts/`: Tests for the `accounts` module (e.g., account creation, retrieval).
- `auth/`: Tests for the `auth` module (e.g., login, token validation).
- `realms/`: Tests for the `realms` module (e.g., realm management, world backups).
- `conftest.py`: Root pytest configurations and shared fixtures.

## Design Patterns

### Pytest Fixture Pattern
Common test dependencies, such as mocked database tables, S3 clients, and API test clients, are provided through pytest fixtures defined in `conftest.py`. This ensures a clean and modular test structure.

### Mocking (Unit Tests)
Unit tests leverage `unittest.mock` to isolate individual components and test them in isolation. This allows for fast and predictable test execution by avoiding external network and database calls.

### Integration Testing
Integration tests verify the correct interaction between multiple modules and their external dependencies (e.g., FastAPI routers and Persistence classes). These tests use `TestClient` to perform HTTP requests and verify responses.
