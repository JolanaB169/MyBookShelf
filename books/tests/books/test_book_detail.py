import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_book_detail_view_get(client, book):
    """
    Test that the book_detail_view returns the book detail page on GET.
    """
    url = reverse("book_detail", args=[book.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["book"] == book
    assert "user_booklists" in response.context

@pytest.mark.django_db
def test_book_detail_view_post_image_upload(client, book, django_user_model):
    """
    Test that posting an image updates the book and redirects.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.force_login(user)

    url = reverse("book_detail", args=[book.id])
    image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
    response = client.post(url, {"image": image})

    book.refresh_from_db()
    # Check that image field is updated
    assert book.image.name.endswith(".jpg")
    assert "test" in book.image.name  # original filename should appear in the saved name
    assert response.status_code == 302
    assert response.url == url

@pytest.mark.django_db
def test_book_detail_view_user_booklists(client, book, django_user_model):
    """
    Test that the view provides the user's booklists with book IDs.
    """
    user = django_user_model.objects.create_user(username="testuser", password="pass")
    client.force_login(user)

    # Create a booklist and add the book
    bl = user.booklists.create(name="My List")
    bl.items.create(book=book)

    url = reverse("book_detail", args=[book.id])
    response = client.get(url)

    user_booklists = response.context["user_booklists"]
    assert len(user_booklists) == 1
    assert user_booklists[0]["list"] == bl
    assert book.id in user_booklists[0]["book_ids"]
