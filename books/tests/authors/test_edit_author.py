import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_edit_author_get(client, author):
    """
    Test that the 'edit_author' view can be accessed via GET
    and that a form is present in the context.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    url = reverse("edit_author", kwargs={"author_id": author.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_edit_author_post(client, author):
    """
    Test that posting valid data to 'edit_author' view updates
    the Author instance and redirects (status code 302).
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    url = reverse("edit_author", kwargs={"author_id": author.pk})
    data = {
        "first_name": "Jane",
        "last_name": author.last_name,
        "country": author.country,
        "year_of_birth": author.year_of_birth,
    }
    response = client.post(url, data)

    # Check that the view redirects after successful POST
    assert response.status_code == 302

    # Check that the author's first name was updated
    author.refresh_from_db()
    assert author.first_name == "Jane"


@pytest.mark.django_db
def test_author_detail_html(client, author):
    """
    Test that the 'author_detail' view renders the author's details
    correctly in the HTML content.
    """
    url = reverse("author_detail", kwargs={"pk": author.pk})
    response = client.get(url)

    assert response.status_code == 200

    content = response.content.decode()
    assert author.first_name in content
    assert author.last_name in content
    if author.year_of_birth:
        assert str(author.year_of_birth) in content
    if getattr(author, "year_of_death", None):
        assert str(author.year_of_death) in content
    if getattr(author, "country", None):
        assert author.country in content
    if getattr(author, "biography", None):
        assert author.biography in content
