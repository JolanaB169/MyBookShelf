import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_register_view_success(client):
    """
    Test that the register_view successfully creates a new user, logs them in,
    and redirects to the home page.
    """
    url = reverse("register")
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "pass1234",
        "password2": "pass1234"
    }
    response = client.post(url, data)

    # Check redirection after successful registration
    assert response.status_code == 302
    assert response.url == reverse("home_page")

    # User account created
    assert User.objects.filter(username="newuser").exists()

    # User is logged in
    user = User.objects.get(username="newuser")
    assert "_auth_user_id" in client.session
    assert int(client.session["_auth_user_id"]) == user.id

@pytest.mark.django_db
def test_register_view_password_mismatch(client):
    """
    Test that the register_view shows an error when the provided passwords do not match.
    """
    url = reverse("register")
    data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "pass123",
        "password2": "different"
    }
    response = client.post(url, data)
    content = response.content.decode()

    # Checking that the page loaded and contains an error message
    assert response.status_code == 200
    assert "Hesla se neshodují" in content

@pytest.mark.django_db
def test_register_view_existing_username(client):
    """
    Test that the register_view shows an error when trying to register with a username that already exists.
    """
    # Create an existing user
    User.objects.create_user(username="existinguser", password="pass123")

    url = reverse("register")
    data = {
        "username": "existinguser",
        "email": "someone@example.com",
        "password": "pass123",
        "password2": "pass123"
    }
    response = client.post(url, data)
    content = response.content.decode()

    # Checking that the page loaded and contains an error message
    assert response.status_code == 200
    assert "Uživatel s tímto jménem již existuje" in content
