from django.db import models
from .authors import Author
from .genre import Genre
from .user import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Book(models.Model):
    """
    Model representing a book and its metadata.
    """
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN", blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    pages = models.PositiveIntegerField(verbose_name="Number of pages", null=True, blank=True)
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    authors = models.ManyToManyField(Author, related_name='books')

    image = models.ImageField(
        upload_to="books/",
        blank=True,
        null=True,
        verbose_name="Obálka knihy"
    )
    approved = models.BooleanField(default=False)

    pending_edit = models.BooleanField(default=False)
    pending_data = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_detail_url(self):
        return f"/book/{self.id}/"