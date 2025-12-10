from django import forms
from books.models import Author


class AuthorForm(forms.ModelForm):
    """
    Form for editing or creating an Author instance.
    Includes fields for country, birth year, death year, and biography.
    """
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'year_of_birth', 'year_of_death', 'country', 'biography']
