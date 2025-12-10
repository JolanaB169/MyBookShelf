import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_edit_book_view_get(client, django_user_model, book):
    """
    Test GET request returns the edit form for a book.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.force_login(user)

    url = reverse("edit_book", args=[book.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["book"] == book


@pytest.mark.django_db
def test_edit_book_view_post_admin_saves_changes(client, django_user_model, book, genre):
    """
    Admin user edits a book: changes are saved directly to the model.
    """
    admin = django_user_model.objects.create_superuser(
        username="admin", password="pass", email="a@b.com"
    )
    client.force_login(admin)

    url = reverse("edit_book", args=[book.id])
    data = {
        "title": "Updated Title",
        "description": "Updated description",
        "genre": [genre.id],  # must provide at least one genre
        "year": 2020,
        "isbn": "1234567890123",
        "publisher": "Test Publisher",
        "pages": 100,
        "new_authors": "Alice Smith",
    }

    response = client.post(url, data)

    book.refresh_from_db()
    assert book.title == "Updated Title"
    assert any(a.first_name == "Alice" for a in book.authors.all())
    assert book.pending_edit is False
    assert book.pending_data is None
    assert response.status_code == 302
    assert response.url == reverse("book_detail", args=[book.id])


@pytest.mark.django_db
def test_edit_book_view_post_regular_user_saves_pending_data(client, django_user_model, book, genre):
    """
    Test POST request by a regular user saves proposed changes to pending_data.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.force_login(user)

    url = reverse("edit_book", args=[book.id])
    data = {
        "title": "Proposed Title",
        "description": "Proposed description",
        "new_authors": "Bob Johnson",
        "genre": [genre.id],
        "year": 2021,
        "isbn": "9876543210123",
        "publisher": "Test Publisher",
        "pages": 150,
    }
    response = client.post(url, data)

    book.refresh_from_db()

    assert book.pending_edit is True
    assert book.pending_data["title"] == "Proposed Title"
    assert book.pending_data["new_authors"]
    assert response.status_code == 302
    assert response.url == reverse("book_detail", args=[book.id])

