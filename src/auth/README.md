# Auth Domain

The `auth` module provides authentication services and JWT-based token management for Helheim.

## Responsibilities

- **Authentication Service:** Verifies user credentials against the account persistence layer.
- **JWT Management:** Generates and decodes access and refresh tokens.
- **Token Security:** Implements password hashing and verification using `pwdlib` (Argon2).
- **Dependencies:** Provides FastAPI dependencies for secure endpoints requiring valid user GUIDs.

## Core Components

- `service.py`: Main `AuthService` class handling login and token refreshing.
- `utils.py`: JWT utilities for encoding/decoding tokens and calculating expiration.
- `dependencies.py`: FastAPI security dependencies (e.g., `get_current_user_guid`).
- `model.py`: Pydantic models for authentication data structures.
