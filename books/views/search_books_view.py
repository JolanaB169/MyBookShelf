from django.shortcuts import render
from ..forms import BookSearchForm
from ..services import search_books

def search_books_view(request):
    """
    View allowing users to search for books using Google Books API.
    """
    results = []
    form = BookSearchForm()

    if request.method == "GET" and "query" in request.GET:
        form = BookSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = search_books(query)

    return render(request, "book_search.html", {
        "form": form,
        "results": results,
    })