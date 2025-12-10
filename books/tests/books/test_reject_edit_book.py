import pytest
from django.urls import reverse
from books.models import Book

@pytest.mark.django_db
def test_reject_book_changes_clears_pending_data(client, admin_user, author):
    """
    Test that reject_book_changes clears pending_data and sets pending_edit to False.
    """
    client.force_login(admin_user)

    book = Book.objects.create(title="Book with Pending Edit", pending_edit=True)
    book.pending_data = {"title": "Proposed Title", "existing_authors": [author.id]}
    book.save()

    url = reverse("reject_edit_book", args=[book.id])
    response = client.get(url)

    book.refresh_from_db()
    assert book.pending_edit is False
    assert book.pending_data is None
    assert response.status_code == 302
    assert response.url == reverse("pending_edits")

@pytest.mark.django_db
def test_reject_book_changes_no_pending_data_shows_warning(client, admin_user):
    """
    Test that if the book has no pending edits, a warning message is shown and redirects to book_detail.
    """
    client.force_login(admin_user)

    book = Book.objects.create(title="Book without Pending Edit", pending_edit=False)

    url = reverse("reject_edit_book", args=[book.id])
    response = client.get(url, follow=True)

    messages = list(response.context["messages"])
    assert any("Žádné čekající změny k zamítnutí" in str(m) for m in messages)
    assert response.status_code == 200
    assert response.request["PATH_INFO"] == reverse("book_detail", args=[book.id])
