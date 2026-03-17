# API Design

Helheim Backend's API is built on FastAPI, following clean architecture principles for routing, dependency management, and error handling.

## Routing

The API is structured into separate routers found in `src/routers/`. Each router handles a specific domain:
-   `/auth`: Authentication and JWT token issuance.
-   `/accounts`: User profile management.
-   `/realms`: Game server realm and world management.

Routers are registered in `src/main.py` using `app.include_router()`.

## Dependency Injection (DI)

FastAPI's built-in dependency injection system is used to provide services and persistence layers to the route handlers. Dependencies are defined in each module's `dependencies.py` or directly in the router files.

Key dependencies include:
-   **Database Access**: `get_account_persistence`, `get_realm_persistence`.
-   **Business Logic**: `get_account_service`, `get_realm_service`, `get_auth_service`.
-   **Cloud Infrastructure**: `get_s3_client`, `get_ec2_client`.

DI ensures that services are decoupled from their implementations, facilitating testing and local development.

## Models and Serialization

All data models for request and response payloads are defined using **Pydantic** in each module's `model.py`. This ensures:
-   Strict data validation.
-   Consistent serialization and deserialization.
-   Automatic documentation generation via OpenAPI (Swagger UI).

## Exception Handling

Custom exceptions are defined in `src/exceptions.py` and module-specific `exceptions.py` files (e.g., `src/accounts/exceptions.py`).

The `register_error_handlers(app)` function in `src/main.py` maps these custom exceptions to HTTP responses with appropriate status codes and JSON payloads. This ensures the API returns consistent error formats for all known failure modes.

### Common Exception Pattern
Custom exceptions inherit from a base `HelheimError` or use specific classes to indicate:
-   `400 Bad Request`: Validation or logic errors.
-   `401 Unauthorized`: Authentication failures.
-   `403 Forbidden`: Insufficient permissions.
-   `404 Not Found`: Resource (account, realm, world) missing.
-   `500 Internal Server Error`: Unhandled system failures.
