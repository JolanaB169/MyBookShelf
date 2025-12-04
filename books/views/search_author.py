from django.shortcuts import render
from books.services.google_books import search_google_books
from ..forms import AuthorSearchForm

def search_author_view(request):
    """
    View for searching books by author.

    Args:
        request (HttpRequest)

    Returns:
        HttpResponse: Renders the author_search.html template with results.
    """
    form = AuthorSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        author_name = form.cleaned_data['author']
        search_query = f"inauthor:{author_name}"
        items = search_google_books(search_query)

        for item in items:
            volume = item.get("volumeInfo", {})
            volume_id = item.get("id")
            if not volume_id:
                continue

            results.append({
                "id": volume_id,
                "title": volume.get("title", "Untitled"),
                "authors": volume.get("authors", []),
                "published_year": volume.get("publishedDate", "N/A"),
                "description": volume.get("description", ""),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail")
            })

    return render(request, "author_search.html", {"form": form, "results": results})