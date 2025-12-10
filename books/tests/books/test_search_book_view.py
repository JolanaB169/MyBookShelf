import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_search_books_view_returns_matching_books(client, book):
    """
    Test that search_books_view returns books matching the query in the title.
    """
    url = reverse("book_search")
    response = client.get(url, {"q": "Test"})

    assert response.status_code == 200
    assert book in response.context["books"]
    assert response.context["query"] == "Test"


@pytest.mark.django_db
def test_search_books_view_empty_query_returns_no_books(client, book):
    """
    Test that an empty search query returns an empty list of books.
    """
    url = reverse("book_search")
    response = client.get(url, {"q": ""})

    assert response.status_code == 200
    assert response.context["books"] == []
    assert response.context["query"] == ""
