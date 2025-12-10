import pytest
from django.urls import reverse
from books.models import Book, BookList, BookListItem
from books.models import Author, Genre
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_booklist_detail_get(client):
    """
    Test GET request to booklist_detail view.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    booklist = BookList.objects.create(name="My List", owner=user)

    # Create a sample book
    author = Author.objects.create(first_name="John", last_name="Doe")
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(title="Book One", description="Desc One")
    book.genre.set([genre])
    book.authors.add(author)

    url = reverse("booklist_detail", kwargs={"list_id": booklist.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "booklist" in response.context
    assert response.context["booklist"] == booklist
    assert "all_books" in response.context
    assert book in response.context["all_books"]


@pytest.mark.django_db
def test_booklist_detail_post_add_book(client):
    """
    Test POST request to add a book to the booklist.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    booklist = BookList.objects.create(name="My List", owner=user)

    # Create a sample book
    author = Author.objects.create(first_name="John", last_name="Doe")
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(title="Book One", description="Desc One")
    book.genre.set([genre])
    book.authors.add(author)

    url = reverse("booklist_detail", kwargs={"list_id": booklist.id})
    response = client.post(url, {"book_id": book.id})

    # Check redirect
    assert response.status_code == 302

    # Check book is in the booklist
    assert BookListItem.objects.filter(booklist=booklist, book=book).exists()
