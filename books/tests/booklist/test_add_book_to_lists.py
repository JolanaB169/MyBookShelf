import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from books.models.books import Book
from books.models.booklist import BookList, BookListItem

@pytest.mark.django_db
def test_add_book_to_list_success(client):
    """
    Test adding a book to a user's booklist successfully.
    """
    user = User.objects.create_user(username="testuser", password="password")
    client.force_login(user)

    book = Book.objects.create(title="Test Book")
    booklist = BookList.objects.create(name="Favorites", owner=user)

    url = reverse("add_book_to_lists", args=[book.id])
    response = client.post(url, {"booklists": [booklist.id]})

    # Redirect expected
    assert response.status_code == 302

    # Check that BookListItem was created
    assert BookListItem.objects.filter(booklist=booklist, book=book).exists()


@pytest.mark.django_db
def test_add_book_to_list_no_selection(client):
    """
    Test posting without selecting any booklists shows warning message.
    """
    from django.contrib.messages import get_messages

    user = User.objects.create_user(username="testuser", password="password")
    client.force_login(user)

    book = Book.objects.create(title="Test Book")

    url = reverse("add_book_to_lists", args=[book.id])
    response = client.post(url, {"booklists": []})

    # Redirect expected
    assert response.status_code == 302

    # Check that no BookListItem was created
    assert BookListItem.objects.filter(book=book).count() == 0

    # Check that warning message is added
    messages = list(get_messages(response.wsgi_request))
    assert any("Musíte vybrat alespoň jeden seznam." in str(m) for m in messages)
