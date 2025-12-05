from django import forms
from .models import UserProfile
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
        fields = ["year", "isbn", "publisher", "pages", "description", "genre", "authors"]
        widgets = {
            "genre": forms.CheckboxSelectMultiple(),
            "authors": forms.CheckboxSelectMultiple(),
        }