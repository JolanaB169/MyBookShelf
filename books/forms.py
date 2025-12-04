from django import forms

class BookSearchForm(forms.Form):
    """ Form used for searching books via Google Books API. """
    query = forms.CharField(label="Search books", max_length=255)

class AuthorSearchForm(forms.Form):
    """
    Form for searching books by author using Google Books API.
    """
    author = forms.CharField(
        label="Author",
        max_length=255,
        required=True,
        help_text="Enter the author's name"
    )