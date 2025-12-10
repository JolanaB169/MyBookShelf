import pytest
from django.urls import reverse
from books.models import Book, Author, Genre

@pytest.mark.django_db
def test_genre_search_with_books(client):
    """
    Test that genre_search_view returns books for a selected genre.
    """
    author = Author.objects.create(first_name="John", last_name="Doe")
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(title="Book One", description="Some description")
    book.authors.add(author)
    book.genre.add(genre)

    url = reverse("genre_search")
    response = client.get(url, {"genre_id": genre.id})

    assert response.status_code == 200
    content = response.content.decode()

    # Check that the book and author appear
    assert "Book One" in content
    assert "John Doe" in content

    # Check that the selected genre is displayed in heading
    assert f'Knihy pro žánr "{genre.name}"' in content

@pytest.mark.django_db
def test_genre_search_no_books(client):
    """
    Test that genre_search_view handles genres with no books.
    """
    genre = Genre.objects.create(name="Non-Fiction")

    url = reverse("genre_search")
    response = client.get(url, {"genre_id": genre.id})

    assert response.status_code == 200
    content = response.content.decode()

    # No books message should appear
    assert "Pro tento žánr nebyly nalezeny žádné knihy." in content
