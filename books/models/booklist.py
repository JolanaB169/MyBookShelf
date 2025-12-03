from django.db import models
from django.contrib.auth.models import User
from .books import Book


class BookList(models.Model):
    """
    A custom list of books created by a logged-in user.
    """
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booklists")

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class BookListItem(models.Model):
    """
    A bridging model connecting books with user-created lists (many-to-many relationship).
    """
    booklist = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="listed_in")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('booklist', 'book')  # a book cannot be added twice to the same list

    def __str__(self):
        return f"{self.book.title} → {self.booklist.name}"