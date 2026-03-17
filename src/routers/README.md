# Routers Module

The **Routers** module defines the API endpoints for the Helheim Backend.

## Components

### `src/routers/auth.py`
Endpoints for authentication:
-   `POST /auth/login`: Handles user authentication and issues a JWT.
-   `POST /auth/refresh`: Refreshes the existing authentication token.

### `src/routers/accounts.py`
Endpoints for account management:
-   `GET /accounts/me`: Retrieves the current user's profile.
-   `PATCH /accounts/me`: Updates the user's account details.
-   `DELETE /accounts/me`: Deletes the user's account.

### `src/routers/realms.py`
Endpoints for realm and world management:
-   `GET /realms`: Lists all realms for the current user.
-   `POST /realms`: Creates a new realm.
-   `GET /realms/{realm_id}`: Retrieves details for a specific realm.
-   `POST /realms/{realm_id}/start`: Starts a game server.
-   `POST /realms/{realm_id}/stop`: Stops a game server.
-   `GET /realms/{realm_id}/worlds`: Lists world files stored on S3.
-   `POST /realms/{realm_id}/worlds/{world_name}/backup`: Creates a backup of a world.
-   `DELETE /realms/{realm_id}/worlds/{world_name}`: Deletes a world file.

### `src/routers/__init__.py`
Exports the routers to be used by the main FastAPI application in `src/main.py`.

## Design Principles

-   **Domain-Specific**: Each router is dedicated to a specific domain (Auth, Accounts, Realms).
-   **Security**: Most routes use the `get_current_active_user` dependency to enforce authentication.
-   **Dependency Injection**: Routers rely on FastAPI's DI to inject the required services and persistence layers.
-   **Validation**: Uses Pydantic models to validate all incoming request bodies and outgoing response data.
-   **Consistency**: Error responses are standardized via custom exceptions and global error handlers.
