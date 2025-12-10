import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Genre, Book
from books.models.user import UserProfile

@pytest.mark.django_db
def test_genre_books_view_get(client, user_with_profile):
    """
    Test GET request: the page should display books of the genre.
    """
    genre = Genre.objects.create(name="Fiction")
    author = Book.objects.create(title="Book One", description="Desc One")
    author.genre.set([genre])

    url = reverse("genre_books", kwargs={"genre_id": genre.id})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert genre.name in content
    assert "Book One" in content


@pytest.mark.django_db
def test_genre_books_view_post_add_remove(client, user_with_profile):
    """
    Test POST request to add and remove genre from user's favorites.
    """
    user = user_with_profile
    client.force_login(user)
    genre = Genre.objects.create(name="Fiction")

    url = reverse("genre_books", kwargs={"genre_id": genre.id})

    # Add genre to favorites
    response = client.post(url, {"action": "add"})
    user.profile.refresh_from_db()
    assert genre in user.profile.favorite_genres.all()
    assert response.status_code == 302

    # Remove genre from favorites
    response = client.post(url, {"action": "remove"})
    user.profile.refresh_from_db()
    assert genre not in user.profile.favorite_genres.all()
    assert response.status_code == 302
