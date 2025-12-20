import pytest
from django.urls import reverse
import re


@pytest.mark.django_db
def test_author_search_html(client, author):
    """
    Test that the 'author_search' view renders correctly via GET,
    displays the search form, and shows results for a valid query.
    Also tests the case when no authors are found.
    """
    url = reverse("author_search")
    response = client.get(url, {"author": "John"})

    # Check that the page returns 200 OK
    assert response.status_code == 200

    content = response.content.decode()

    # Check that the search form exists
    assert '<form method="get">' in content
    assert 'name="author"' in content
    assert 'Hledat' in content

    # Check that the search result contains the author
    assert "John Doe" in content

    # Test empty search (no authors found)
    response_empty = client.get(url, {"author": "Neexistující"})
    content_empty = response_empty.content.decode()
    assert "Žádní autoři nenalezeni." in content_empty


@pytest.mark.django_db
def test_author_search_links(client, author):
    """
    Test that the search results contain links to the correct
    'author_detail' view and that the author's name appears inside <a> tags.
    """
    url = reverse("author_search")
    response = client.get(url, {"author": "John"})

    assert response.status_code == 200
    content = response.content.decode()

    # Check that the link points to the correct author detail page
    expected_url = reverse(
        "author_detail",
        kwargs={"pk": author.pk}
    )
    assert expected_url in content

    # Regex to check the author's name inside <a> tag
    pattern = re.compile(rf">[\s]*{author.first_name} {author.last_name}[\s]*</a>")
    assert pattern.search(content)