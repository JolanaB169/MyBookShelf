import pytest
import os
from django.urls import reverse

@pytest.mark.django_db
def test_author_detail_get(client, author):
    """
    Test that the 'author_detail' view can be accessed via GET,
    and that the context contains the correct author and related books.
    """
    url = reverse("author_detail", kwargs={"pk": author.pk})

    response = client.get(url)
    assert response.status_code == 200
    assert "author" in response.context
    assert response.context["author"] == author
    assert "db_books" in response.context
    assert list(response.context["db_books"]) == list(author.books.all())


@pytest.mark.django_db
def test_author_detail_view(client, author):
    """
    Test that the 'author_detail' view renders correctly
    and that the author's details appear in the HTML content.
    """
    url = reverse("author_detail", kwargs={"pk": author.pk})
    response = client.get(url)

    assert response.status_code == 200

    content = response.content.decode()
    assert author.first_name in content
    assert author.last_name in content
    assert str(author.year_of_birth) in content


@pytest.mark.django_db
def test_author_detail_upload_photo(client, author, tmp_path):
    """
    Test that uploading a photo via the 'author_detail' view
    correctly saves the file and updates the author's photo field.
    """
    url = reverse("author_detail", kwargs={"pk": author.pk})

    # Create a fake image file
    image_path = tmp_path / "test.jpg"
    image_path.write_bytes(b"fake image content")

    # Post the file
    with open(image_path, "rb") as img:
        response = client.post(url, {"photo": img})

    assert response.status_code in (200, 302)

    author.refresh_from_db()
    filename = os.path.basename(author.photo.name)
    assert filename.startswith("test")
    assert filename.endswith(".jpg")
