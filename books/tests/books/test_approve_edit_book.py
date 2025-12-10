import pytest
from django.urls import reverse
from books.models import Book, Author

@pytest.mark.django_db
def test_approve_book_changes_applies_pending_data(client, admin_user):
    """
    Test that approve_book_changes applies pending edits and updates the book.
    """
    # Log in as admin
    client.login(username="admin", password="pass")

    # Create a book with pending edits
    book = Book.objects.create(title="Original Title", approved=False)
    pending_author = Author.objects.create(first_name="Jane", last_name="Doe")

    # Set pending data for approval
    book.pending_edit = True
    book.pending_data = {
        "title": "Updated Title",
        "existing_authors": [pending_author.id]
    }
    book.save()

    # Call the approval view
    url = reverse("approve_edit_book", args=[book.id])
    response = client.get(url)

    # Refresh from DB and assert changes
    book.refresh_from_db()
    assert book.title == "Updated Title"  # title updated
    assert pending_author in book.authors.all()  # author added
    assert book.approved is True  # book marked as approved
    assert book.pending_edit is False  # pending_edit cleared
    assert book.pending_data is None  # pending_data cleared
    assert response.status_code == 302  # redirected

@pytest.mark.django_db
def test_approve_book_changes_no_pending_data_shows_warning(client, admin_user):
    """
    Test that approving a book without pending data shows a warning message.
    """
    # Log in as admin
    client.login(username="admin", password="pass")

    # Create a book without pending edits
    book = Book.objects.create(title="Book without pending edit", approved=False)

    # Call the approval view with follow=True to capture messages
    url = reverse("approve_edit_book", args=[book.id])
    response = client.get(url, follow=True)

    # Assert that a warning message is shown
    messages = list(response.context["messages"])
    assert any("Žádné změny čekající na schválení" in str(m) for m in messages)
    assert response.status_code == 200
