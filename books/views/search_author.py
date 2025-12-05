from django.shortcuts import render
from books.models import Author

def search_author_view(request):
    """
    Search authors by first or last name and display results.
    """
    query = request.GET.get("author", "")
    results = []

    if query:
        results = Author.objects.filter(
            first_name__icontains=query
        ) | Author.objects.filter(
            last_name__icontains=query
        )

    return render(request, "author_search.html", {"results": results, "query": query})
