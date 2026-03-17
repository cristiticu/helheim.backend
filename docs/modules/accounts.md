# Accounts Module

The `accounts` module handles user account creation, management, and basic profile information. It is one of the foundation modules for Helheim's user-centric features.

## 🧱 Components

### 1. `model.py`
Defines the structure of a user account.
- **Account**: The core internal model containing `guid`, `username`, `password` (hashed), and `c_at` (creation date).
- **AccountDto**: The public Data Transfer Object (DTO) used for API responses (excludes the sensitive password hash).
- **CreateAccount**: The input validation model for new accounts.

### 2. `persistence.py`
Handles interactions with the **DynamoDB** `helheim.table.authentication` table.
- **Key Pattern**: Uses a simple primary key (`guid`) but maintains a Global Secondary Index (`gsi.username`) for fast lookups by username.
- **Methods**:
  - `persist(payload: Account)`: Saves a new account.
  - `get_by_guid(guid: UUID4)`: Retrieves an account by its unique ID.
  - `get_by_username(username: str)`: Retrieves an account via the `gsi.username` index.

### 3. `service.py`
Contains the business logic for accounts.
- **`AccountService`**: Coordinates between `AccountsPersistence` and `AuthService`.
- **Functionality**:
  - `create_account(...)`: Hashes passwords, checks for existing usernames, and generates a unique GUID before persisting.

## 🔌 API Endpoints (via `routers/accounts.py`)

- `POST /accounts`: Create a new user account.
- `GET /accounts/me`: (In progress/planned) Retrieve the current user's details.

## 🛠 Patterns and Specifics

- **Password Hashing**: Passwords must never be stored in plain text. The `AuthService` handles hashing using `pwdlib`.
- **Validation**: All account creations are validated for unique usernames at the service layer.
- **Single Source of Truth**: The `AccountsPersistence` is the only component allowed to touch the authentication DynamoDB table directly.
- **Pydantic mapping**: Models include `to_db_item()` and `from_db_item()` methods to handle the serialization between Pydantic and DynamoDB dictionary formats.
