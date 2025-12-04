from django.shortcuts import render
from books.services.google_books import search_google_books
from ..forms import BookSearchForm

def search_books_view(request):
    """
       View for searching books using the Google Books API.

       Args:
           request (HttpRequest): The Django request object containing GET parameters.

       Returns:
           HttpResponse: Renders the book_search.html template with the search form
                         and a list of search results.
       """
    # Initialize the search form with GET data
    form = BookSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        items = search_google_books(query)

        # Process each book returned by Google Books
        for item in items:
            volume = item.get("volumeInfo", {})
            volume_id = item.get("id")
            if not volume_id:
                continue  # skip books without an ID

            results.append({
                "id": volume_id,
                "title": volume.get("title", "Bez názvu"),
                "authors": volume.get("authors", []),
                "published_year": volume.get("publishedDate", "N/A"),
                "description": volume.get("description", ""),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail")
            })

    # Render the search template with form and results
    return render(request, "book_search.html", {"form": form, "results": results})