import pytest
from django.urls import reverse
from books.models import UserProfile, BookList, Author, Genre

@pytest.mark.django_db
def test_profile_view_get(client, django_user_model):
    """
    Test that the profile page loads correctly and displays user profile data.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    UserProfile.objects.create(user=user)
    client.login(username="testuser", password="pass")

    url = reverse("profile")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert "profile" in response.context
    assert response.context["profile"].user == user

    # decode content to check non-ASCII characters
    content = response.content.decode("utf-8")
    assert "Profil uživatele: testuser" in content

@pytest.mark.django_db
def test_profile_view_post_updates_reading_goal(client, django_user_model):
    """
    Test that POST updates the reading_goal of the user profile.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    profile = UserProfile.objects.create(user=user, reading_goal=5)
    client.login(username="testuser", password="pass")

    url = reverse("profile")
    response = client.post(url, {"reading_goal": 10})

    profile.refresh_from_db()
    assert profile.reading_goal == 10
    assert response.status_code == 302
    assert response.url == url

@pytest.mark.django_db
def test_profile_view_displays_favorite_genres_and_authors(client, django_user_model):
    """
    Test that favorite genres and preferred authors are rendered in the profile.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    profile = UserProfile.objects.create(user=user)

    genre = Genre.objects.create(name="Fiction")
    author = Author.objects.create(first_name="John", last_name="Doe")

    profile.favorite_genres.add(genre)
    profile.preferred_authors.add(author)
    client.login(username="testuser", password="pass")

    url = reverse("profile")
    response = client.get(url)
    content = response.content.decode()

    assert genre.name in content
    assert f"{author.first_name} {author.last_name}" in content

@pytest.mark.django_db
def test_profile_view_displays_booklists(client, django_user_model):
    """
    Test that the user's booklists are rendered on the profile page.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    profile = UserProfile.objects.create(user=user)

    booklist = BookList.objects.create(name="My List", owner=user)
    client.login(username="testuser", password="pass")

    url = reverse("profile")
    response = client.get(url)
    content = response.content.decode()

    assert booklist.name in content
    assert "Vytvořit nový seznam" in content
