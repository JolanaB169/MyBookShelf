import pytest
from django.contrib.auth.models import User
from books.models import Author, Book, UserProfile, Genre

@pytest.fixture
def user(db):
    """Creates a test user."""
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def author(db):
    """Creates a test author."""
    return Author.objects.create(
        first_name="John",
        last_name="Doe",
        country="USA",
        year_of_birth=1970
    )

@pytest.fixture
def book(db, author):
    """Creates a test book with an author."""
    book = Book.objects.create(
        title="Test Book",
        description="Some description"
    )
    book.authors.add(author)
    return book

@pytest.fixture
def user_with_profile(django_user_model):
    user = django_user_model.objects.create_user(username="testuser", password="password")

    UserProfile.objects.create(user=user)

    return user

@pytest.fixture
def genre(db):
    """Creates a test genre."""
    return Genre.objects.create(name="Fiction")


@pytest.fixture
def admin_user(db, django_user_model):
    """
    Creates a superuser for tests.
    """
    return django_user_model.objects.create_superuser(
        username="admin", password="pass", email="admin@example.com"
    )