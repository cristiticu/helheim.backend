# Realms Module

The `realms` module is the core of Helheim. It manages the creation, configuration, and state of game server instances (Portals).

## 🧱 Components

### 1. `model.py`
The module defines multiple specialized Pydantic models for its entities:
- **Realm**: Represents a high-level game community or server cluster.
- **RealmUser**: Links a user to a specific Realm with a defined role (e.g., owner, member).
- **RealmPortal**: Represents an active or historical game server instance.
- **RealmWorld**: Represents a game world file saved in S3.
- **RealmListFile**: Used to manage configuration files like "adminlist.txt", "bannedlist.txt", etc.
- **Modifiers**: Pydantic `Literal` and `Union` types for Valheim-specific world settings (`CombatModifier`, `RaidsModifier`, etc.).

### 2. `persistence.py`
The `RealmsPersistence` class manages a complex set of interactions:
- **Single Table Design**: Uses `helheim.table.realms` with the following `s_key` (Sort Key) patterns:
  - `REALM#DETAILS`: Stores `Realm` data.
  - `USER#<user_guid>`: Stores `RealmUser` data.
  - `PORTAL#<portal_guid>`: Stores `RealmPortal` data.
- **S3 Integration**: Interacts with the `helheim.storage` bucket for world files and list files.
- **WorldManager**: A specialized component for handling S3-based world file operations (backup, delete, list).

### 3. `service.py`
The `RealmsService` coordinates the lifecycle of game servers:
- **Methods**:
  - `open_portal(...)`: The most complex operation. It triggers the Lambda-based instance management, sets up world configurations, and records the `RealmPortal` in DynamoDB.
  - `close_portal(...)`: Marks a portal as closing and triggers instance termination.
  - `get_realms_for_user(...)`: Queries the `gsi.user-realms-lookup-2` index to find all realms associated with a user.
  - `manage_realm_files(...)`: Handles the upload and retrieval of game-specific configuration files (lists).

### 4. `world_manager.py`
A low-level utility class for managing S3 keys related to game worlds. It handles the directory structure inside the `helheim.storage` bucket.

### 5. `exceptions.py`
Defines module-specific errors like `RealmNotFound`, `WorldNotFound`, or `PortalNotFound`.

## 🔌 API Endpoints (via `routers/realms.py`)

- `GET /realms`: List all realms the current user belongs to.
- `GET /realms/{realm_guid}`: Get details of a specific realm.
- `GET /realms/{realm_guid}/portals`: List active and historical portals for a realm.
- `POST /realms/{realm_guid}/portals`: Open a new portal (start a game server).
- `DELETE /realms/{realm_guid}/portals/{portal_guid}`: Close a portal (stop a game server).
- `GET /realms/{realm_guid}/worlds`: List available game world files in S3.
- `GET /realms/{realm_guid}/lists/{file_name}`: Retrieve a configuration list file.
- `POST /realms/{realm_guid}/lists`: Update a configuration list file.

## 🛠 Patterns and Specifics

### 1. Instance Management via Lambda
The backend doesn't directly manage EC2 instances. Instead, it invokes a specialized Lambda (`VALHEIM_INSTANCE_LAMBDA_NAME` or `VINTAGE_STORY_INSTANCE_LAMBDA_NAME`). This pattern keeps the API lightweight and secure.

### 2. World Modifiers (Valheim)
The `CreateRealmPortal` model supports extensive Valheim world modifiers. These are passed to the instance management Lambda to configure the game environment on startup.

### 3. S3 Folder Structure
World data is stored in S3 using the pattern:
`{realm_guid}/worlds/{world_name}/...`
This ensures data isolation between different realms.

### 4. DynamoDB Query Patterns
- To find all users in a realm: `query(PartitionKey=realm_guid, SortKey.begins_with("USER#"))`.
- To find all portals in a realm: `query(PartitionKey=realm_guid, SortKey.begins_with("PORTAL#"))`.
- To find a specific user's relationship to a realm: `get_item(PartitionKey=realm_guid, SortKey="USER#" + user_guid)`.
