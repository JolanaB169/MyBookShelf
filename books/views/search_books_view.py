from django.shortcuts import render
from books.models import Book, Author
from django.db.models import Q

def search_books_view(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query)
        ).distinct()

    return render(request, "book_search.html", {"books": results, "query": query})

