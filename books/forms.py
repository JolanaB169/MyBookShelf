from django import forms

class BookSearchForm(forms.Form):
    """ Form used for searching books via Google Books API. """
    query = forms.CharField(label="Search books", max_length=255)
