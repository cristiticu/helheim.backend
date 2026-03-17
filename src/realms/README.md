# Realms Domain

The `realms` module is the core of Helheim, managing game servers (Realms) and portals for Valheim and Vintage Story.

## Responsibilities

- **Realm Lifecycle:** Managing realms, game worlds, and world backups.
- **Portal Management:** Opening and closing game server instances via EC2 Spot Instances.
- **Game Server Integration:** Invoking specific AWS Lambda functions (`VALHEIM_INSTANCE_LAMBDA_NAME`, `VINTAGE_STORY_INSTANCE_LAMBDA_NAME`) to provision and configure game servers.
- **Realm Configuration:** Managing realm-specific list files (permitted, banned, and admin lists).
- **Persistence:** Storing realm metadata and active portal status in DynamoDB.

## Core Components

- `service.py`: `RealmsService` class handling high-level business logic for portal management and realm operations.
- `persistence.py`: `RealmsPersistence` class for CRUD operations on DynamoDB's realms table.
- `world_manager.py`: (Optional/Extended logic) Logic for managing specific game worlds within a realm.
- `model.py`: Comprehensive Pydantic models for `Realm`, `RealmPortal`, `RealmWorld`, and server configuration payloads.
- `dependencies.py`: FastAPI dependencies for accessing realm-specific data.
- `exceptions.py`: Domain-specific exceptions like `PortalAlreadyOpened`, `PasswordTooShort`, and `InvalidRealmListFileName`.

## Portal Opening Workflow

1. Validate realm and check for existing open portals.
2. Invoke the game-specific AWS Lambda (Valheim or Vintage Story).
3. The Lambda provisioned an EC2 Spot Instance and returns connection details.
4. The `RealmsService` persists a `RealmPortal` object with the instance details, public IP, and connection parameters.
