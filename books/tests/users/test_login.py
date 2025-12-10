import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login_view_success(client):
    """
    Test successful login redirects to the profile page.
    """
    user = User.objects.create_user(username="john", password="pass123")
    url = reverse("login")

    response = client.post(url, {"username": "john", "password": "pass123"})

    # Should redirect to profile
    assert response.status_code == 302
    assert response.url == reverse("profile")

@pytest.mark.django_db
def test_login_view_failure(client):
    """
    Test login failure shows error message.
    """
    url = reverse("login")
    response = client.post(url, {"username": "wrong", "password": "wrongpass"}, follow=True)

    # Page should render again with error message
    assert response.status_code == 200
    content = response.content.decode()
    assert "Neplatné jméno nebo heslo" in content
