# Realms Module

The **Realms** module provides game server orchestration and world management for Helheim Backend.

## Components

### `src/realms/model.py`
Defines data models for realms and worlds:
-   `Realm`: The core realm structure, including its `guid`, `realm_type` (e.g., `valheim`, `vintage_story`), and current state.
-   `RealmWorld`: The representation of an individual world file on S3.
-   `RealmCreate`, `RealmUpdate`: Request schemas for realm management.

### `src/realms/persistence.py`
Provides the `RealmPersistence` class for DynamoDB access:
-   `create_realm`: Persists new realm configurations.
-   `get_realm`: Retrieves realm information by ID.
-   `list_realms`: Queries all realms associated with an account.
-   `update_realm`, `delete_realm`: Modifies realm data or deletes a realm.

### `src/realms/service.py`
Implements business logic for managing realms, including state transitions and interactions with the `WorldManager`.

### `src/realms/world_manager.py`
The **`WorldManager`** class handles interactions with S3 for game world data. It contains the logic for different game types:

1.  **Valheim**: Uses a dual-file system (`.db` and `.fwl`).
2.  **Vintage Story**: Uses a single file (`.vcdbs`).

**Key Responsibilities**:
-   `get_worlds(realm)`: Lists all worlds for a given realm by prefix-searching S3.
-   `backup_world(realm, world_name, backup_name)`: Copies world files within S3 to create a snapshot.
-   `delete_world(realm, world_name)`: Permanently removes all files associated with a specific world from S3.

### `src/realms/dependencies.py`
Provides dependencies for injecting realm-related services:
-   `get_realm_service`: Injects the `RealmService`.
-   `get_realm_persistence`: Injects the `RealmPersistence`.
-   `get_world_manager`: Injects the `WorldManager` with a configured S3 client.

### `src/realms/exceptions.py`
Contains module-specific exceptions such as `RealmNotFound`, `WorldNotFound`, or `InvalidRealmType`.

## Interaction Flow
1.  **Orchestration**: A request to start a realm is received by the router.
2.  **Service Call**: `RealmService` coordinates with `RealmPersistence` to retrieve state and updates the realm's status.
3.  **World Management**: If a user requests a world backup, the `RealmService` delegates the task to the `WorldManager`.
4.  **S3 Operation**: The `WorldManager` performs the specific file operations (copying `.db/.fwl` or `.vcdbs`) based on the `realm_type`.
5.  **Response**: The service returns the updated realm or world information.
