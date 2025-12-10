import pytest
from django.urls import reverse
from books.models import Author
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_add_author_view_get(client):
    """
    Test that the 'add_author' view renders correctly via GET request
    and includes a form in the context.
    """
    user = User.objects.create_user(username="testuser", password="password")
    client.force_login(user)

    url = reverse("add_author")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_add_author_view_post_valid(client):
    """
    Test that posting valid data to 'add_author' view creates
    a new Author record and redirects (status code 302).
    """
    user = User.objects.create_user(username="testuser", password="password")
    client.force_login(user)

    url = reverse("add_author")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "year_of_birth": 1980,
        "year_of_death": "",
        "country": "USA",
        "biography": "Some bio"
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert Author.objects.filter(first_name="John", last_name="Doe").exists()


@pytest.mark.django_db
def test_add_author_creates_record():
    """
    Test that creating an Author instance directly via the model
    successfully stores it in the database.
    """
    author = Author.objects.create(
        first_name="Jane",
        last_name="Smith",
        year_of_birth=1975,
        country="UK",
        biography="Biography text"
    )
    assert Author.objects.filter(id=author.id).exists()
