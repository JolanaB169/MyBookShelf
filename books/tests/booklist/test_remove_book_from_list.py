import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Book, Author, Genre
from books.models.booklist import BookList, BookListItem


@pytest.mark.django_db
def test_remove_book_from_list_success(client):
    """
    Test removing a book from a booklist successfully.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    # Create booklist and book
    booklist = BookList.objects.create(name="My List", owner=user)
    author = Author.objects.create(first_name="John", last_name="Doe")
    genre = Genre.objects.create(name="Fiction")
    book = Book.objects.create(title="Book One", description="Desc One")
    book.genre.set([genre])
    book.authors.add(author)

    # Add book to list
    item = BookListItem.objects.create(booklist=booklist, book=book)

    url = reverse("remove_book_from_list", kwargs={"list_id": booklist.id, "book_id": book.id})
    response = client.get(url)  # usually redirect views are GET or POST, here GET works

    # Check redirect
    assert response.status_code == 302

    # Book should no longer be in list
    assert not BookListItem.objects.filter(id=item.id).exists()


@pytest.mark.django_db
def test_remove_book_from_list_not_found(client):
    """
    Test removing a book that is not in the list raises 404.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    booklist = BookList.objects.create(name="My List", owner=user)

    # Book ID that does not exist
    url = reverse("remove_book_from_list", kwargs={"list_id": booklist.id, "book_id": 999})

    response = client.get(url)
    assert response.status_code == 404
