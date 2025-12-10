import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_logout_clears_session(client):
    """
    Verifies that the logout_view properly clears the user's session.
    Ensures that after accessing the logout URL, the user is no longer authenticated.
    """
    user = User.objects.create_user(username="testuser", password="pass")
    client.login(username="testuser", password="pass")

    # Before logout, session contains the user
    assert "_auth_user_id" in client.session

    url = reverse("logout")
    response = client.get(url)

    # After logout, the session should no longer contain the user
    assert "_auth_user_id" not in client.session

@pytest.mark.django_db
def test_logout_redirects_to_home(client):
    """
    Ensures that after logout, the user is redirected to the home page.
    Checks that the response status code is 302 and the redirect URL is correct.
    """
    user = User.objects.create_user(username="testuser", password="pass")
    client.login(username="testuser", password="pass")

    url = reverse("logout")
    response = client.get(url)

    # Verify redirection to home page
    assert response.status_code == 302
    assert response.url == reverse("home_page")
