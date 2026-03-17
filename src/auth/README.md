# Auth Module

The **Auth** module provides authentication and security for the Helheim Backend.

## Components

### `src/auth/model.py`
Defines data models for:
-   `UserLoginRequest`: Payload for login attempts.
-   `Token`: The structure of the generated JWT.
-   `TokenPayload`: Data stored within the JWT (e.g., `user_id`, `exp`).

### `src/auth/service.py`
Contains the core authentication logic:
-   `authenticate_user`: Validates user credentials.
-   `create_access_token`: Generates a JWT using the application's secret key.
-   `get_current_user`: Extracts and validates the token from the request header.

### `src/auth/utils.py`
Provides utility functions for security-related tasks:
-   `verify_password`: Comparing a plain-text password against a hashed version.
-   `get_password_hash`: Generating a secure hash from a plain-text password.

### `src/auth/dependencies.py`
FastAPI dependencies used in routers to enforce security:
-   `get_auth_service`: Provides the `AuthService`.
-   `get_current_active_user`: Validates the token and ensures the user account is active.

## Interaction Flow
1.  **Login**: User sends credentials to `/auth/login`.
2.  **Authentication**: `AuthService` verifies the credentials and, if valid, returns a JWT.
3.  **Authorized Requests**: For subsequent requests to protected endpoints, the client includes the JWT in the `Authorization: Bearer <token>` header.
4.  **Token Validation**: The `get_current_active_user` dependency parses the header, validates the signature, and retrieves the account.
5.  **Access Granted**: If valid, the route handler proceeds with the authorized user object.
