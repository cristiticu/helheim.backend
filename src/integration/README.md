# Integration Module

The **Integration** module contains components and scripts for setting up the Helheim Backend for local development and integration testing.

## Components

### `src/integration/create-db.local.sh`
A shell script for initializing a local DynamoDB instance with the required table schemas. It creates the following tables:
-   `Accounts`: Stores user profiles and credentials.
-   `Realms`: Stores game server configuration and status.

### `run.local.sh`
The main entry point for running the Helheim Backend locally. It sets up environment variables (e.g., `TABLE_NAME`, `REGION`, `ENDPOINT_URL`) and starts the FastAPI application via `uvicorn`.

## Setup for Local Development

1.  **Start a Local Database**:
    -   Use Docker to run a DynamoDB container: `docker run -p 8000:8000 amazon/dynamodb-local`
    -   Or use LocalStack for a full AWS emulation.

2.  **Initialize Tables**:
    ```bash
    ./src/integration/create-db.local.sh
    ```

3.  **Run the Application**:
    ```bash
    ./run.local.sh
    ```
    The API will be available at `http://localhost:8000`.

## Testing Integration

Integration tests use these local resources to verify the interaction between the FastAPI routers and the persistent storage layers. While unit tests use `moto` for mocking, integration tests can be run against real (local) DynamoDB and S3 instances to ensure compatibility.
