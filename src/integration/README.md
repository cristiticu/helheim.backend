# Integration Module

## Purpose
The `integration` module contains code and scripts for integration testing, local database setup, and infrastructure orchestration.

## Structure
- `create-db.local.sh`: A shell script for setting up a local DynamoDB instance (e.g., via Docker or LocalStack) and creating tables and GSIs.

## Design Patterns

### Local Development Environment
The `create-db.local.sh` script automates the creation of DynamoDB tables and GSIs to match the single-table design used in production. This ensures that developers can run and test the application locally without needing access to a real AWS environment.

### Infrastructure-as-Code (IaC)
While not directly using Terraform or CDK within this module, the shell scripts provide a basic form of IaC to maintain consistency between development, testing, and production environments.
