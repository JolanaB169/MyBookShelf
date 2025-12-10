import pytest
from django.urls import reverse
from books.models import Book, Genre, Author


@pytest.mark.django_db
def test_book_list_view_all_books(client):
    """
    Test that book_list_view returns all books when no filters are applied.
    """
    author = Author.objects.create(first_name="John", last_name="Doe")
    genre = Genre.objects.create(name="Fiction")

    book1 = Book.objects.create(title="Book One", description="Desc One")
    book1.genre.set([genre])
    book1.authors.add(author)

    book2 = Book.objects.create(title="Book Two", description="Desc Two")
    book2.genre.set([genre])
    book2.authors.add(author)

    url = reverse("book_list")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Book One" in content
    assert "Book Two" in content


@pytest.mark.django_db
def test_book_list_view_filter_by_title(client):
    """
    Test that book_list_view correctly filters books by title.
    """
    author = Author.objects.create(first_name="John", last_name="Doe")
    genre = Genre.objects.create(name="Fiction")

    book1 = Book.objects.create(title="Book One", description="Desc One")
    book1.genre.set([genre])
    book1.authors.add(author)

    book2 = Book.objects.create(title="Another Book", description="Desc Two")
    book2.genre.set([genre])
    book2.authors.add(author)

    url = reverse("book_list")
    response = client.get(url, {"title": "Book One"})

    assert response.status_code == 200
    content = response.content.decode()
    assert "Book One" in content
    assert "Another Book" not in content
