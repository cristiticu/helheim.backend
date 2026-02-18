import uuid


def test_get_user_realms_success(client, realms_table, seeded_realm, seeded_realm_user_member, auth_header):
    # When: GET /realm with valid token
    resp = client.get("/realm", headers=auth_header)

    # Then
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    assert item["guid"] == seeded_realm["guid"]
    assert item["user_guid"] == seeded_realm_user_member["user_guid"]
    assert item["role"] == "member"


def test_get_user_realms_empty(client, auth_header, realms_table):
    # When: user has no realms
    resp = client.get("/realm", headers=auth_header)

    # Then
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_realm_requires_membership(client, seeded_realm, auth_header):
    # When: user without realm membership tries to access realm
    resp = client.get(f"/realm/{seeded_realm['guid']}", headers=auth_header)

    # Then
    assert resp.status_code == 403
    assert resp.json()["message"].lower(
    ) == "user does not have access to this realm"


def test_get_realm_success(client, seeded_realm, seeded_realm_user_member, auth_header):
    resp = client.get(f"/realm/{seeded_realm['guid']}", headers=auth_header)

    assert resp.status_code == 200
    data = resp.json()
    assert data["guid"] == seeded_realm["guid"]
    assert data["name"] == seeded_realm["name"]
    assert data["meta_type"] == "REALM"


def test_get_realm_users_success(client, seeded_realm, seeded_realm_user_admin, auth_header):
    resp = client.get(
        f"/realm/{seeded_realm['guid']}/user", headers=auth_header)

    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)
    assert len(users) >= 1
    assert users[0]["guid"] == seeded_realm_user_admin["guid"]


def test_get_realm_file_success(client, seeded_list_file_adminlist, seeded_realm, seeded_realm_user_member, auth_header):
    resp = client.get(
        f"/realm/{seeded_realm['guid']}/file/{seeded_list_file_adminlist['file_name']}", headers=auth_header
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["file_name"] == seeded_list_file_adminlist["file_name"]
    assert "content" in data


def test_get_realm_file_not_found(client, seeded_realm, seeded_realm_user_member, auth_header, realms_bucket):
    resp = client.get(
        f"/realm/{seeded_realm['guid']}/file/unknown.txt", headers=auth_header
    )
    assert resp.status_code == 404
    assert resp.json()["message"].lower() == "failed to get realm list file"


def test_create_list_file_success_admin(client, seeded_realm, seeded_realm_user_admin, auth_header, realms_bucket):
    payload = {"file_name": "permittedlist.txt", "content": "user1"}
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/file",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["message"].lower() == "file created successfully"


def test_create_list_file_forbidden_member(client, seeded_realm, seeded_realm_user_member, auth_header, realms_bucket):
    payload = {"file_name": "adminlist.txt", "content": "user1"}
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/file",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 403


def test_create_list_file_invalid_name(client, seeded_realm, seeded_realm_user_admin, auth_header):
    payload = {"file_name": "invalid.txt", "content": "x"}
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/file",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert "invalid realm list file name" in resp.json()["message"].lower()


def test_get_realm_worlds_valheim(client, realms_bucket, seeded_realm, seeded_realm_user_member, seeded_world_valheim, auth_header):
    resp = client.get(
        f"/realm/{seeded_realm['guid']}/world", headers=auth_header)
    assert resp.status_code == 200
    worlds = resp.json()
    assert isinstance(worlds, list)
    assert any(w["name"] == seeded_world_valheim for w in worlds)


def test_get_realm_worlds_vintage(client, realms_bucket, seeded_realm_vintage, seeded_realm_user_member, seeded_world_vintage, auth_header):
    resp = client.get(
        f"/realm/{seeded_realm_vintage['guid']}/world", headers=auth_header)
    assert resp.status_code == 200
    worlds = resp.json()
    assert any(w["name"] == seeded_world_vintage for w in worlds)


def test_create_world_backup_success(client, realms_bucket, seeded_realm, seeded_realm_user_admin, seeded_world_valheim, auth_header):
    backup_name = "MidgardBackup"
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/world/{seeded_world_valheim}/backup",
        json={"backup_name": backup_name},
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["message"].lower() == "backup created successfully"


def test_create_world_backup_not_found(client, seeded_realm, seeded_realm_user_admin, auth_header, realms_bucket):
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/world/NoWorld/backup",
        json={"backup_name": "NoBackup"},
        headers=auth_header,
    )
    assert resp.status_code == 404
    # Service includes specific world + realm in message; assert semantic meaning
    assert "not found" in resp.json()["message"].lower()


def test_delete_realm_world_success(client, realms_bucket, seeded_realm, seeded_realm_user_admin, seeded_world_valheim, auth_header):
    resp = client.delete(
        f"/realm/{seeded_realm['guid']}/world/{seeded_world_valheim}",
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["message"].lower() == "world deleted successfully"


def test_get_portals_list(client, seeded_realm, seeded_realm_user_member, seeded_portal, auth_header):
    resp = client.get(
        f"/realm/{seeded_realm['guid']}/portal", headers=auth_header)
    assert resp.status_code == 200
    portals = resp.json()
    assert isinstance(portals, list)
    assert len(portals) == 1


def test_open_realm_portal_success_admin(client, seeded_realm, seeded_realm_user_admin, auth_header, stub_lambda_invocation):
    payload = {"name": "Srv", "world_name": "World", "password": "secretpw"}
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/portal",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 200
    portal = resp.json()
    assert portal["guid"] == seeded_realm["guid"]
    assert portal["world_name"] == "World"
    assert portal["status"] in ("running", "pending")


def test_open_realm_portal_already_opened(client, seeded_realm, seeded_realm_user_admin, seeded_portal, auth_header):
    payload = {"name": "Srv", "world_name": "World", "password": "anotherpw"}
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/portal",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert "already open" in resp.json()["message"].lower()


def test_open_realm_portal_password_too_short(client, seeded_realm, seeded_realm_user_admin, auth_header):
    payload = {"name": "Srv", "world_name": "World", "password": "123"}
    resp = client.post(
        f"/realm/{seeded_realm['guid']}/portal",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 400
    assert "password is too short" in resp.json()["message"].lower()


def test_close_realm_portal_success(client, seeded_realm, seeded_realm_user_admin, seeded_portal, auth_header):
    payload = {
        "portal_guid": seeded_portal["s_key"].split("#")[1],
        "instance_id": seeded_portal["instance_id"],
        "spot_request_id": seeded_portal["spot_request_id"],
    }
    resp = client.request(
        "DELETE",
        f"/realm/{seeded_realm['guid']}/portal",
        json=payload,
        headers=auth_header,
    )
    assert resp.status_code == 200
    assert resp.json()["message"].lower() == "portal closed successfully"
