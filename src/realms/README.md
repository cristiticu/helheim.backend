# Realms Module

## Purpose
The `realms` module handles game realms, portal management, and world backups. It is responsible for organizing the core game infrastructure and user-realm relationships.

## Structure
- `model.py`: Pydantic models for realms, portals, and world data.
- `service.py`: `RealmsService` class containing business logic for realm management (e.g., world backup orchestration, portal creation).
- `persistence.py`: `RealmsPersistence` class (Repository Pattern) for interacting with DynamoDB and S3.
- `world_manager.py`: Utilities for handling world-related files and backups on S3.
- `dependencies.py`: FastAPI dependencies for realm-specific route protection.
- `exceptions.py`: Module-specific exceptions (e.g., `RealmNotFound`, `WorldNotFound`).

## Design Patterns

### Repository Pattern
The `RealmsPersistence` class encapsulates all data access logic. It interacts with both DynamoDB (for realm metadata and relationships) and Amazon S3 (for world files and lists). This abstraction allows the service layer to work with high-level `Realm`, `RealmUser`, and `RealmWorld` objects.

### Single-Table Design
The `realms` module extensively uses DynamoDB Single-Table Design.
- `REALM#DETAILS`: Stores metadata for a specific realm.
- `USER#<user_guid>`: Stores relationship data between a user and a realm.
- `PORTAL#<portal_guid>`: Stores portal configuration.

A Global Secondary Index (GSI) on `user_guid` allows for efficient querying of all realms a specific user belongs to.

### Service Layer Separation
`RealmsService` provides a high-level API for realm operations, orchestrating complex tasks like managing world backups and handling user permissions within a realm.
