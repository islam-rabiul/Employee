from datetime import datetime


def test_create_user_success(client):
    """Test successful user creation."""
    response = client.post(
        "/user/",
        json={
            "name": "Islam Rabi",
            "email": "islamrabi79@gmail.com",
            "date": datetime.now().isoformat(),
            "password": "234890",
            "domain": "Engineering"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "islamrabi79@gmail.com"
    assert "id" in data


def test_create_user_validation_failure(client):
    """Test validation failure (e.g., malformed email)."""
    response = client.post(
        "/user/",
        json={
            "name": "Invalid User",
            "email": "not-an-email",
            "date": datetime.now().isoformat(),
            "password": "123",
            "domain": "HR"
        }
    )
    assert response.status_code == 422


def test_get_user_not_found(client):
    """Test getting a user ID that doesn't exist (404 Not Found)."""
    response = client.get("/user/id/999")
    assert response.status_code == 404


def test_get_all_users(client):
    """Test fetching all user records."""
    # First, create a user
    client.post(
        "/user/",
        json={
            "name": "Alice Smith",
            "email": "alice@example.com",
            "date": datetime.now().isoformat(),
            "password": "password123",
            "domain": "Finance"
        }
    )

    response = client.get("/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_user_by_id_and_email(client):
    """Test fetching a specific user by ID and by Email."""
    # Create user
    create_res = client.post(
        "/user/",
        json={
            "name": "Bob Jones",
            "email": "bob@example.com",
            "date": datetime.now().isoformat(),
            "password": "password123",
            "domain": "Marketing"
        }
    )
    user_id = create_res.json()["id"]

    # Test Get by ID
    id_res = client.get(f"/user/id/{user_id}")
    assert id_res.status_code == 200
    assert id_res.json()["email"] == "bob@example.com"

    # Test Get by Email
    email_res = client.get("/user/email/bob@example.com")
    assert email_res.status_code == 200
    assert email_res.json()["id"] == user_id


def test_update_user(client):
    """Test updating user details."""
    create_res = client.post(
        "/user/",
        json={
            "name": "Charlie",
            "email": "charlie@example.com",
            "date": datetime.now().isoformat(),
            "password": "password123",
            "domain": "Sales"
        }
    )
    user_id = create_res.json()["id"]

    # Update user name
    update_res = client.put(
        f"/user/id/{user_id}",
        json={"name": "Charlie Updated"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Charlie Updated"


def test_delete_user(client):
    """Test deleting a user."""
    create_res = client.post(
        "/user/",
        json={
            "name": "David",
            "email": "david@example.com",
            "date": datetime.now().isoformat(),
            "password": "password123",
            "domain": "Support"
        }
    )
    user_id = create_res.json()["id"]

    # Delete user
    delete_res = client.delete(f"/user/id/{user_id}")
    assert delete_res.status_code == 200

    # Verify user is gone (should return 404)
    get_res = client.get(f"/user/id/{user_id}")
    assert get_res.status_code == 404