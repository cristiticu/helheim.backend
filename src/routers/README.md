# Routers Module

## Purpose
The `routers` module contains FastAPI router definitions, providing the public API interface for the application.

## Structure
- `accounts.py`: Endpoints for user account management (e.g., registration, profile).
- `auth.py`: Endpoints for user authentication and login.
- `realms.py`: Endpoints for realm, portal, and world management.
- `__init__.py`: Exports routers for integration in `main.py`.

## Design Patterns

### FastAPI Router Pattern
The module uses `APIRouter` to modularize the application's API. This allows for clean separation of endpoints by functional domain and easy integration into the main FastAPI application instance.

### Dependency Injection
Routers heavily leverage FastAPI's dependency injection system to inject `Service` and `Persistence` classes into endpoint handlers. This ensures a clear flow of control and simplifies unit and integration testing.

### DTO (Data Transfer Object) Pattern
Endpoints use Pydantic models for both request validation (e.g., `CreateAccount`) and response serialization (e.g., `AccountDTO`). This pattern ensures that internal database models are never directly exposed to the API consumer.
