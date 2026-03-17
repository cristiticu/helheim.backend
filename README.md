# Helheim Backend

Helheim is a backend service designed to manage game server instances (Valheim, Vintage Story) on AWS. It provides a FastAPI-based REST API to handle user accounts, authentication, and realm (server) management, including automated deployment of game servers using AWS EC2 Spot Instances and Lambda.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web framework.
- **Server Gateway:** [Mangum](https://mangum.io/) - Adapter for running ASGI applications in AWS Lambda.
- **Cloud Provider:** [AWS](https://aws.amazon.com/) (DynamoDB, S3, EC2, Lambda).
- **SDK:** [Boto3](https://aws.amazon.com/sdk-for-python/) - AWS SDK for Python.
- **Environment Management:** [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver.
- **Security:** [pwdlib](https://github.com/the-maldridge/pwdlib) (Argon2), [PyJWT](https://pyjwt.readthedocs.io/).

## Architecture

The project follows a modular domain-driven structure:

- **src/auth:** Authentication logic, JWT token generation, and verification.
- **src/accounts:** User account management and persistence.
- **src/realms:** Core logic for managing game servers (Realms), including portal opening/closing via EC2 and Lambda.
- **src/shared:** Shared utilities and AWS client wrappers (DynamoDB, S3, EC2, Lambda).
- **src/routers:** FastAPI route definitions mapping HTTP endpoints to domain services.

Deployment is primarily targeted at AWS Lambda using Mangum, with DynamoDB for persistence and S3 for storage.

## Developer Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) installed.
- AWS CLI configured with appropriate credentials.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cristiticu/helheim.backend.git
   cd helheim.backend
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Running Locally

1. Set up your environment variables. Create a `.env.local` file based on the requirements in `src/settings.py`.
   ```bash
   export ENVIRONMENT=local
   ```

2. Run the local development server:
   ```bash
   ./run.local.sh
   ```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
