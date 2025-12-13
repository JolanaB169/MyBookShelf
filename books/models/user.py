from django.db import models
from django.contrib.auth.models import User
from .genre import Genre
from .authors import Author

class UserProfile(models.Model):
    """
    Additional optional profile information for each user, focused on reading preferences.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    favorite_genres = models.ManyToManyField(Genre, blank=True, related_name="fans")
    preferred_authors = models.ManyToManyField(Author, blank=True, related_name="followers")
    reading_goal = models.PositiveIntegerField(
        null=True, blank=True, help_text="Kolik knih plánuješ letos přečíst"
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
