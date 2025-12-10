from django import forms
from books.models import BookList


class BookListForm(forms.ModelForm):
    """Formulář pro vytvoření nebo úpravu uživatelského seznamu knih."""
    class Meta:
        model = BookList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Název seznamu"}),
        }