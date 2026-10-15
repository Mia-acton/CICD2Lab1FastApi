import pytest


def user_payload(
    name="Paul",
    email="paul@atu.ie",
    age=25,
    sid="S1234567",
):
    return {
        "name": name,
        "email": email,
        "age": age,
        "student_id": sid,
    }


def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()

    # The database generates the ID.
    assert isinstance(data["id"], int)
    assert data["name"] == "Paul"
    assert data["email"] == "paul@atu.ie"
    assert data["student_id"] == "S1234567"


def test_duplicate_user_returns_409(client):
    first_response = client.post("/api/users", json=user_payload())
    assert first_response.status_code == 201

    # Sending the same email and student ID again should fail.
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()


@pytest.mark.parametrize(
    "bad_student_id",
    ["1234567", "s1234567", "S123", "S12345678"],
)
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post(
        "/api/users",
        json=user_payload(sid=bad_student_id),
    )

    assert response.status_code == 422


def test_get_users_returns_created_users(client):
    created = client.post(
        "/api/users",
        json=user_payload(name="Alice", email="alice@atu.ie"),
    )
    assert created.status_code == 201
    user_id = created.json()["id"]

    response = client.get("/api/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == user_id
    assert data[0]["name"] == "Alice"


def test_get_existing_user_returns_200(client):
    created = client.post("/api/users", json=user_payload())
    assert created.status_code == 201
    user_id = created.json()["id"]

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_existing_user_returns_204(client):
    created = client.post("/api/users", json=user_payload())
    assert created.status_code == 201
    user_id = created.json()["id"]

    response = client.delete(f"/api/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""  # A 204 response has no body.


def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_deleted_user_can_no_longer_be_retrieved(client):
    created = client.post("/api/users", json=user_payload())
    assert created.status_code == 201
    user_id = created.json()["id"]

    deleted = client.delete(f"/api/users/{user_id}")
    assert deleted.status_code == 204

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 404