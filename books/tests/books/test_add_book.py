import pytest
from django.urls import reverse
from books.models import Book


@pytest.mark.django_db
def test_add_book_view_get(client, django_user_model):
    """Test that add_book_view returns the form page for GET requests."""
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.login(username="testuser", password="pass")

    url = reverse("add_book_view")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_add_book_view_post_existing_authors(client, django_user_model, author, genre):
    """Test that add_book_view creates a book with existing authors on POST."""
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.login(username="testuser", password="pass")

    url = reverse("add_book_view")
    data = {
        "title": "New Book",
        "description": "A test book",
        "existing_authors": [author.id],
        "genre": [genre.id],  # ManyToMany field expects a list of IDs
    }
    response = client.post(url, data)

    book = Book.objects.get(title="New Book")
    assert book.created_by == user
    assert author in book.authors.all()
    assert book.approved
    assert response.status_code == 302
    assert response.url == reverse("book_list")


@pytest.mark.django_db
def test_add_book_view_post_new_authors(client, django_user_model, genre):
    """Test that add_book_view creates a book and adds new authors entered inline."""
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.login(username="testuser", password="pass")

    url = reverse("add_book_view")
    data = {
        "title": "Another Book",
        "description": "Book with new authors",
        "new_authors": "Alice Smith\nBob Johnson",
        "genre": [genre.id],
    }
    response = client.post(url, data)

    book = Book.objects.get(title="Another Book")
    assert book.created_by == user
    # Checking that new authors have been created
    author_names = [(a.first_name, a.last_name) for a in book.authors.all()]
    assert ("Alice", "Smith") in author_names
    assert ("Bob", "Johnson") in author_names
    assert book.approved
    assert response.status_code == 302
    assert response.url == reverse("book_list")
