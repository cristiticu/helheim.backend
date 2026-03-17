# Auth Module

## Purpose
The `auth` module provides authentication and authorization services. It handles user login, token generation (JWT), and route protection.

## Structure
- `model.py`: Pydantic models for authentication payloads (e.g., login, tokens).
- `service.py`: `AuthService` class containing business logic for user authentication.
- `dependencies.py`: FastAPI dependencies for route protection (e.g., `get_current_user`).
- `utils.py`: Utility functions for JWT creation, password hashing, and token validation.

## Design Patterns

### Repository Pattern
While the `auth` module primarily focuses on logic and security, it interacts with the `AccountsPersistence` layer through its dependency on `AccountsService`.

### Service Layer Separation
`AuthService` is responsible for authenticating users by validating credentials and generating JSON Web Tokens (JWTs). It abstracts the complexities of password verification and token creation.

### OAuth2 Password Flow
Authentication is implemented following the OAuth2 Password Flow with Bearer Tokens. The `dependencies.py` module uses `OAuth2PasswordBearer` to extract and validate tokens from HTTP headers.
