from django.shortcuts import render
from books.models import Book
from books.forms import AuthorSearchForm

def search_author_view(request):
    form = AuthorSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        author_name = form.cleaned_data['author']
        results = Book.objects.filter(
            authors__first_name__icontains=author_name
        ) | Book.objects.filter(
            authors__last_name__icontains=author_name
        )

    return render(request, "author_search.html", {"form": form, "results": results})
