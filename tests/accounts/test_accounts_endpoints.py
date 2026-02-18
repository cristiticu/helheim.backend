import uuid


def test_get_account_success(client, seeded_account, auth_header, accounts_table):
    # When: GET /account/{guid} with a valid token
    resp = client.get(
        f"/account/{seeded_account['guid']}", headers=auth_header)

    # Then
    assert resp.status_code == 200
    data = resp.json()

    assert data["guid"] == seeded_account["guid"]
    assert data["username"] == seeded_account["username"]
    assert "c_at" in data
    # Ensure sensitive fields are not present
    assert "password" not in data


def test_get_account_not_found(client, auth_header, accounts_table):
    # Given: a guid that does not exist
    missing_guid = str(uuid.uuid4())

    # When
    resp = client.get(f"/account/{missing_guid}", headers=auth_header)

    # Then
    assert resp.status_code == 404
    assert resp.json()["message"].lower() == "account not found"


def test_get_account_requires_auth(client, seeded_account):
    # When: missing Authorization header
    resp = client.get(f"/account/{seeded_account['guid']}")

    # Then
    assert resp.status_code == 401
