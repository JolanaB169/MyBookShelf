from django import forms
from .models import UserProfile, Author
from .models.books import Book



class UserProfileForm(forms.ModelForm):
    """
    Form for updating the user's profile information.
    Allows the user to upload a profile photo and set a yearly reading goal.
    """
    class Meta:
        model = UserProfile
        fields = ["photo", "reading_goal"]
        widgets = {
            "favorite_genres": forms.CheckboxSelectMultiple(),
            "preferred_authors": forms.CheckboxSelectMultiple(),
        }

class BookForm(forms.ModelForm):
    """
    Form for editing or creating a Book instance.
    Allows selection of multiple genres and authors via checkboxes.
    """
    class Meta:
        model = Book
        fields = ["title", "year", "isbn", "publisher", "pages", "description", "genre", "authors"]
        widgets = {
            "genre": forms.CheckboxSelectMultiple(),
            "authors": forms.CheckboxSelectMultiple(),
        }

class AuthorForm(forms.ModelForm):
    """
    Form for editing or creating an Author instance.
    Includes fields for country, birth year, death year, and biography.
    """
    class Meta:
        model = Author
        fields = ["country", "year_of_birth", "year_of_death", "biography"]
