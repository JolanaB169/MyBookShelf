from django.shortcuts import render
from books.models import Book, Author
from django.db.models import Q

def search_books_view(request):
    """Search books by title and display the results."""

    query = request.GET.get("q", "")
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query)
        ).distinct()

    return render(request, "book_search.html", {"books": results, "query": query})

