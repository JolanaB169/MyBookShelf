import pytest
from django.urls import reverse
from books.models import Book

@pytest.mark.django_db
def test_pending_edits_view_status_and_context(client, admin_user):
    """
    Test that the pending_edits_view returns 200 and provides the correct context.
    Only accessible by staff users.
    """
    client.force_login(admin_user)

    url = reverse("pending_edits")
    response = client.get(url)

    assert response.status_code == 200
    assert "books" in response.context

@pytest.mark.django_db
def test_pending_edits_view_filters_books(client, admin_user):
    """
    Test that only books with pending_edit=True appear in the view.
    """
    client.force_login(admin_user)

    # Create books
    book1 = Book.objects.create(title="Pending Book", pending_edit=True)
    book2 = Book.objects.create(title="Approved Book", pending_edit=False)

    url = reverse("pending_edits")
    response = client.get(url)
    books_in_context = response.context["books"]

    assert book1 in books_in_context
    assert book2 not in books_in_context
