from django.db import models
from .authors import Author
from .genre import Genre
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Book(models.Model):
    """
    Model representing a book and its metadata.
    """
    STAR_CHOICES = (
        (0, '0 Stars'),
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star')
    )
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publisher = models.CharField(max_length=100, blank=True, null=True)
    pages = models.PositiveIntegerField(verbose_name="Number of pages", null=True, blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)])
    genre = models.ManyToManyField(Genre)
    rating = models.IntegerField(choices=STAR_CHOICES, default=0)
    description = models.TextField()
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.title