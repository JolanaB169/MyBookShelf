import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from books.models.booklist import BookList

@pytest.mark.django_db
def test_create_booklist_get(client):
    """
    Test GET request to create_booklist view: the form should be displayed.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    url = reverse("create_booklist")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_create_booklist_post_valid(client):
    """
    Test POST request to create a new booklist.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_login(user)

    url = reverse("create_booklist")
    data = {"name": "My New List"}
    response = client.post(url, data)

    # Redirect after successful creation
    assert response.status_code == 302
    assert BookList.objects.filter(name="My New List", owner=user).exists()
