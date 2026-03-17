# Accounts Module

## Purpose
The `accounts` module manages user accounts, including creation, retrieval, and deletion. It serves as the primary system for user identity management within the platform.

## Structure
- `model.py`: Pydantic models for account data, defining DTOs (Data Transfer Objects) and database models.
- `service.py`: `AccountsService` class containing business logic for account management (e.g., password hashing, validation).
- `persistence.py`: `AccountsPersistence` class (Repository Pattern) for interacting with DynamoDB.
- `exceptions.py`: Module-specific exceptions (e.g., `AccountNotFound`, `UsernameAlreadyExists`).

## Design Patterns

### Repository Pattern
The `AccountsPersistence` class abstracts all direct DynamoDB calls. It uses `boto3` to perform `put_item`, `get_item`, `query`, and `delete_item` operations. It also handles mapping between DynamoDB items and Pydantic models.

### Service Layer Separation
`AccountsService` orchestrates the account creation process. It performs high-level validations (e.g., checking for username uniqueness) and handles password hashing using `pwdlib`. It depends on `AccountsPersistence` for data storage.

### Single-Table Design
Accounts are stored in a DynamoDB table. We use a Global Secondary Index (GSI) on `username` to allow for efficient lookups by username during the login and registration processes.
