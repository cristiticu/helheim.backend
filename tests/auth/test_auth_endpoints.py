import uuid
from datetime import datetime, timezone, timedelta

from auth.utils import create_access_token


def test_authenticate_success(client, accounts_table, seeded_account):
    # When: POST /auth with valid credentials
    resp = client.post(
        "/auth",
        data={"username": seeded_account["username"],
              "password": seeded_account["password"]},
    )

    # Then
    assert resp.status_code == 200
    data = resp.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_authenticate_unknown_user(client, accounts_table):
    # When: POST /auth with unknown username
    resp = client.post(
        "/auth",
        data={"username": "nouser", "password": "whatever"},
    )

    # Then
    assert resp.status_code == 401
    assert resp.json()["message"].lower() == "invalid credentials"


def test_authenticate_wrong_password(client, accounts_table, seeded_account):
    # When: POST /auth with wrong password
    resp = client.post(
        "/auth",
        data={"username": seeded_account["username"], "password": "wrong"},
    )

    # Then
    assert resp.status_code == 401
    assert resp.json()["message"].lower() == "invalid credentials"


def test_authenticate_missing_fields(client):
    # When: POST /auth with missing fields -> 422 from FastAPI validation
    resp = client.post("/auth", data={"username": "user"})

    # Then
    assert resp.status_code == 422


def test_register_success(client, accounts_table):
    # When: POST /auth/register with a new username
    resp = client.post(
        "/auth/register",
        json={"username": "newuser", "password": "NewPass!234"},
    )

    # Then
    assert resp.status_code == 200
    data = resp.json()

    assert "guid" in data
    assert data["username"] == "newuser"
    assert "c_at" in data


def test_register_duplicate_username(client, accounts_table):
    # Given: existing user
    client.post(
        "/auth/register",
        json={"username": "dupeuser", "password": "Pass!234"},
    )

    # When: register same username
    resp = client.post(
        "/auth/register",
        json={"username": "dupeuser", "password": "Another!234"},
    )

    # Then
    assert resp.status_code == 400
    assert resp.json()["message"].lower() == "username already exists"


def test_refresh_success(client, accounts_table, seeded_account):
    # Given: a valid refresh token for the seeded user
    token = create_access_token(
        {"user_guid": seeded_account["guid"]}, expire=5)

    # When: POST /auth/refresh with Authorization: Bearer <token>
    resp = client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {token}"})

    # Then
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_expired_token(client, accounts_table, seeded_account):
    # Given: an expired token (expire negative)
    token = create_access_token(
        {"user_guid": seeded_account["guid"]}, expire=-1)

    # When
    resp = client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {token}"})

    # Then
    assert resp.status_code == 401
    assert resp.json()["message"].lower() == "expired signature"


def test_refresh_corrupt_token(client):
    # When: POST /auth/refresh with corrupt token
    resp = client.post(
        "/auth/refresh", headers={"Authorization": "Bearer invalid.token.value"})

    # Then
    assert resp.status_code == 401
    assert resp.json()["message"].lower() == "corrupt signature"
