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
    Allows selection of multiple genres via checkboxes.
    Allows selection of existing authors via checkboxes and adding new authors inline.
    """
    # Existing authors can be selected via checkboxes
    existing_authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Vyberte existující autory"
    )

    # New authors can be added as text (one per line)
    new_authors = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Každý autor na nový řádek'}),
        label="Noví autoři"
    )

    class Meta:
        model = Book
        fields = [
            "title", "year", "isbn", "publisher", "pages",
            "description", "genre"
        ]
        widgets = {
            "genre": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        """
        When loading the form, it pre-populates existing_authors by book
        but does not access the authors field directly!
        """
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["existing_authors"].initial = self.instance.authors.all()


class AuthorForm(forms.ModelForm):
    """
    Form for editing or creating an Author instance.
    Includes fields for country, birth year, death year, and biography.
    """
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'year_of_birth', 'year_of_death', 'country', 'biography']