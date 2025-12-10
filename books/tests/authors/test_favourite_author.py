import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_favorite_author_add(client, user_with_profile, author):
    """
    Test that posting to 'favorite_author' view adds the author
    to the user's preferred authors and redirects (status code 302).
    """
    client.login(username="testuser", password="password")

    url = reverse("favorite_author", args=[author.id])
    response = client.post(url)

    # Refresh user profile to get updated preferred authors
    user_with_profile.profile.refresh_from_db()

    # Check that the author is now in preferred authors
    assert author in user_with_profile.profile.preferred_authors.all()

    # Check that the response is a redirect
    assert response.status_code == 302


@pytest.mark.django_db
def test_favorite_author_remove(client, user_with_profile, author):
    """
    Test that posting to 'favorite_author' view removes the author
    from the user's preferred authors and redirects (status code 302).
    """
    # First, add the author to preferred authors
    user_with_profile.profile.preferred_authors.add(author)

    client.login(username="testuser", password="password")

    url = reverse("favorite_author", args=[author.id])
    response = client.post(url)

    user_with_profile.profile.refresh_from_db()

    # Check that the author was removed from preferred authors
    assert author not in user_with_profile.profile.preferred_authors.all()

    # Check that the response is a redirect
    assert response.status_code == 302
