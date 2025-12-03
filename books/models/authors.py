from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Author(models.Model):
    """
    Model representing a book author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=120, blank=True, null=True)
    year_of_birth = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(datetime.datetime.now().year)])
    year_of_death = models.IntegerField(validators=[MinValueValidator(1900),
                                                    MaxValueValidator(datetime.datetime.now().year)],
                                        blank=True, null=True)
    biography = models.TextField(blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"