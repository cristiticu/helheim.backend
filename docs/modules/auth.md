# Authentication Module

The `auth` module provides the security layer for Helheim. It manages tokens, login, and access control.

## 🧱 Components

### 1. `model.py`
- **LoginPayload**: The input structure for the `/auth/token` endpoint (`username` and `password`).
- **TokenResponse**: The DTO for successful logins containing `access_token` and `refresh_token`.
- **RefreshPayload**: The input for refreshing expired access tokens.

### 2. `utils.py`
Handles low-level JWT operations:
- **`create_access_token(...)`**: Signs a payload with a secret key using the specified algorithm (HS256).
- **`decode_access_token(...)`**: Verifies and decodes a JWT token string.

### 3. `service.py`
The core logic for user authentication:
- **`AuthService`**: Coordinates with `AccountsPersistence`.
- **Methods**:
  - `authenticate(username, password)`: Verifies user credentials and issues tokens.
  - `refresh(refresh_token, user_guid)`: Re-issues a token set if the refresh token is valid and matches the user.

### 4. `dependencies.py`
FastAPI dependencies used to secure endpoints:
- **`get_current_user(...)`**: Extracts the user GUID from the Bearer token in the request header.
- **Usage**: Typically injected into routers as `Depends(get_current_user)`.

## 🔌 API Endpoints (via `routers/auth.py`)

- `POST /auth/token`: Exchanges credentials for a JWT access/refresh token pair.
- `POST /auth/refresh`: Exchanges a refresh token for a new set of tokens.

## 🛠 Patterns and Specifics

- **JWT Structure**: Tokens contain the `user_guid` in the payload (sub).
- **Expiration**: Token TTL (Time-To-Live) is defined in `settings.py`.
- **Statelessness**: The backend does not store session state in a database; it relies solely on JWT validation.
- **Security Protocols**: All sensitive endpoints must use the `get_current_user` dependency.
- **Hashing**: Uses `pwdlib` for password verification (Argon2 or similar recommended standards).
- **Secret Key Management**: The `SECRET_KEY` is loaded from the environment and should be rotated regularly in production.
