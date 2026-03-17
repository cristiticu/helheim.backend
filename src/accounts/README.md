# Accounts Module

The **Accounts** module handles user profile and account management.

## Components

### `src/accounts/model.py`
Defines the `Account` and `AccountPreference` Pydantic models for request and response validation.

### `src/accounts/persistence.py`
Provides the `AccountPersistence` class, which implements data access logic for DynamoDB. It handles:
-   `create_account`: Registering new accounts.
-   `get_account`: Retrieving an account by ID.
-   `update_account`: Modifying account details or preferences.
-   `delete_account`: Removing an account.

### `src/accounts/service.py`
Implements the business logic for account management, acting as an intermediary between the router and persistence layer.

### `src/accounts/exceptions.py`
Contains module-specific exceptions like `AccountNotFound` or `AccountAlreadyExists`.

## Interaction Flow
1.  **Router**: Receives an account-related HTTP request.
2.  **Dependency Injection**: Injects the `AccountService`.
3.  **Service**: Validates business logic and calls the `AccountPersistence` layer.
4.  **Persistence**: Interacts with DynamoDB to read or write data.
5.  **Response**: The service returns the processed account data or raises a specific exception.
