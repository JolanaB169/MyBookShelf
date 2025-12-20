from django import forms
from books.models import BookList


class BookListForm(forms.ModelForm):
    """Form for creating or editing a user's book list."""
    class Meta:
        model = BookList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Název seznamu"}),
        }