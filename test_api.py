import requests

BASE_URL = "http://localhost:5000"

USERNAME = "apitest"
EMAIL = "apitest@example.com"
PASSWORD = "testpass"


# Helper functions (not collected by pytest)
def api_register():
    reg_data = {"username": USERNAME, "email": EMAIL, "password": PASSWORD}
    r = requests.post(f"{BASE_URL}/register", json=reg_data)
    assert r.status_code in (201, 409)
    return r

def api_login():
    login_data = {"username": USERNAME, "password": PASSWORD}
    r = requests.post(f"{BASE_URL}/login", json=login_data)
    assert r.status_code == 200
    assert "access_token" in r.json()
    return r.json()["access_token"]

def api_create_post(token):
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {"title": "pytest post", "content": "pytest content"}
    r = requests.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
    assert r.status_code == 201
    assert "post_id" in r.json()
    return r.json()["post_id"]


# Test functions (collected by pytest)
def test_register():
    r = api_register()
    if r.status_code == 201:
        assert r.json().get("msg") == "User created"
    elif r.status_code == 409:
        assert r.json().get("msg") == "User already exists"

def test_register_missing_fields():
    reg_data = {"username": USERNAME}
    r = requests.post(f"{BASE_URL}/register", json=reg_data)
    assert r.status_code == 400

def test_register_invalid_email():
    """Test registering with an invalid email format."""
    reg_data = {"username": "bademail", "email": "notanemail", "password": "testpass"}
    r = requests.post(f"{BASE_URL}/register", json=reg_data)
    assert r.status_code == 400

def test_login():
    token = api_login()
    assert token

def test_login_wrong_password():
    login_data = {"username": USERNAME, "password": "wrongpass"}
    r = requests.post(f"{BASE_URL}/login", json=login_data)
    assert r.status_code == 400 or r.status_code == 401

def test_create_post():
    token = api_login()
    post_id = api_create_post(token)
    assert post_id

def test_create_post_no_token():
    post_data = {"title": "pytest post", "content": "pytest content"}
    r = requests.post(f"{BASE_URL}/posts", json=post_data)
    assert r.status_code == 401

def test_create_post_invalid_data():
    token = api_login()
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {"title": ""}  # missing content
    r = requests.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
    assert r.status_code == 400

def test_create_post_sql_injection():
    """Test creating a post with SQL injection attempt in the title."""
    token = api_login()
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {"title": "' OR 1=1 --", "content": "sql injection test"}
    r = requests.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
    # Should be rejected as invalid input or just treated as a string, but not cause an error
    assert r.status_code in (201, 400)

def test_get_posts():
    r = requests.get(f"{BASE_URL}/posts")
    assert r.status_code == 200
    assert "posts" in r.json()

def test_update_post():
    token = api_login()
    post_id = api_create_post(token)
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"title": "updated title", "content": "updated content"}
    r = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data, headers=headers)
    assert r.status_code == 200

def test_update_post_no_token():
    token = api_login()
    post_id = api_create_post(token)
    update_data = {"title": "updated title", "content": "updated content"}
    r = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data)
    assert r.status_code == 401

def test_update_post_invalid_id():
    token = api_login()
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"title": "updated title", "content": "updated content"}
    r = requests.put(f"{BASE_URL}/posts/999999", json=update_data, headers=headers)
    assert r.status_code == 404

def test_delete_post():
    token = api_login()
    post_id = api_create_post(token)
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
    assert r.status_code == 200

def test_delete_post_no_token():
    token = api_login()
    post_id = api_create_post(token)
    r = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert r.status_code == 401

def test_delete_post_invalid_id():
    token = api_login()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{BASE_URL}/posts/999999", headers=headers)
    assert r.status_code == 404

def test_protected_endpoint_with_malformed_token():
    """Test accessing a protected endpoint with a malformed JWT token."""
    headers = {"Authorization": "Bearer not.a.valid.token"}
    r = requests.post(f"{BASE_URL}/posts", json={"title": "test", "content": "test"}, headers=headers)
    assert r.status_code == 422

def test_unauthorized_create_post():
    """
    Test that creating a post without a JWT token returns 401 Unauthorized.
    """
    post_data = {"title": "unauth post", "content": "should fail"}
    r = requests.post(f"{BASE_URL}/posts", json=post_data)
    assert r.status_code == 401
    assert "error" in r.json() or "msg" in r.json()


# Security note: In production, never hardcode secrets or credentials in code. Use environment variables and strong passwords.
# Note: For full isolation, run your Flask app with a test config using a separate test database.
# Example: Set DATABASE_URL=sqlite:///test_api.db in your test environment.

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
