from django import forms
from books.models import Author, Book


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
