# Helheim Backend Documentation

Welcome to the official documentation for the **Helheim Backend**. This repository serves as the central API for managing Valheim and Vintage Story game servers (realms), user accounts, and authentication.

This documentation is designed to be the "gold standard" for AI agents and developers working on this codebase.

## 🏗 Architecture Overview

Helheim Backend is a **FastAPI** application designed to run in a serverless environment (AWS Lambda) using **Mangum**. It follows a modular monolith pattern with a clear separation of concerns between routers, services, and persistence layers.

### Key Technologies
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Runtime**: AWS Lambda (via Mangum)
- **Database**: DynamoDB (Single Table Design patterns)
- **Storage**: AWS S3 (World data, modpacks, lists)
- **Compute**: AWS EC2 (Game servers managed via Lambda)
- **Validation**: Pydantic v2
- **Package Management**: `uv`

## 📁 Project Structure

```text
src/
├── accounts/      # User account management (models, service, persistence)
├── auth/          # Authentication logic (JWT, OAuth2 dependencies)
├── realms/        # Core logic for game servers (Realms, Portals, Worlds)
├── routers/       # API endpoints grouped by module
├── shared/        # Shared utilities and AWS client wrappers
├── main.py        # Application entry point & middleware configuration
├── settings.py    # Environment-based configuration
├── exceptions.py  # Global error handling and mapping
└── context.py     # Execution context (correlation IDs, etc.)
```

## 🛠 Design Patterns

### 1. Layers of Concern
- **Routers**: Handle HTTP requests, input validation (Pydantic), and call Services.
- **Services**: Contain business logic. They are responsible for coordinating between persistence and external integrations.
- **Persistence**: Abstract the database (DynamoDB) and storage (S3). They handle the mapping between DB items and Pydantic models.
- **Models**: Pydantic classes that define the data structures for both the API (DTOs) and the Database (Items).

### 2. Single Table Design (DynamoDB)
The project utilizes DynamoDB with specific `s_key` (Sort Key) patterns to store multiple entity types in the same table (especially in the `realms` module).
- `REALM#DETAILS`: Primary realm information.
- `USER#<user_guid>`: Links a user to a realm.
- `PORTAL#<portal_guid>`: Represents an active or historical game server instance.

### 3. Error Handling
A global exception handling mechanism is used. Modules define their own exceptions (e.g., `RealmNotFound`), which are caught and converted to appropriate HTTP responses in `src/exceptions.py`.

## 🚀 Getting Started

### Environment Configuration
The application uses the `ENVIRONMENT` variable to load `.env.<env>` files.
Supported values: `local`, `production`, `test`.

### Dependency Management
This project uses `uv`. To install dependencies:
```bash
uv sync
```

### Local Development
Run the local development server:
```bash
./run.local.sh
```

## 📚 Module Documentation

- [Accounts Module](./modules/accounts.md)
- [Authentication Module](./modules/auth.md)
- [Realms Module](./modules/realms.md)
- [Shared Utilities](./modules/shared.md)
