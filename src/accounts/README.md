# Accounts Domain

The `accounts` module manages user profiles and persistence in Helheim.

## Responsibilities

- **Account Management:** Creating, retrieving, and deleting user accounts.
- **Persistence:** Direct interaction with DynamoDB to store and retrieve user account data.
- **Validation:** Ensures username uniqueness and validates account data structures.
- **DTO Transformation:** Converts internal account models to Data Transfer Objects (DTOs) for external responses.

## Core Components

- `service.py`: `AccountsService` class for business logic related to user accounts.
- `persistence.py`: `AccountsPersistence` class for CRUD operations on DynamoDB's authentication table.
- `model.py`: Pydantic models for `Account` (internal) and `CreateAccount` (input).
- `exceptions.py`: Domain-specific exceptions like `AccountNotFound` and `UsernameAlreadyExists`.
