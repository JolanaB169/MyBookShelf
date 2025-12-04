from django.shortcuts import render
from books.services.google_books import search_google_books

def author_detail_view(request, author_name):
    """
    View to display all books by a specific author using Google Books API.

    Args:
        request (HttpRequest)
        author_name (str): The name of the author.

    Returns:
        HttpResponse: Renders the author_detail.html template with the author's books.
    """
    items = search_google_books(author_name)
    books = []

    for item in items:
        volume = item.get("volumeInfo", {})
        volume_id = item.get("id")
        title = volume.get("title", "Untitled")
        if volume_id:
            books.append({
                "id": volume_id,
                "title": title,
                "published_year": volume.get("publishedDate", "N/A"),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail")
            })

    context = {
        "author_name": author_name,
        "books": books
    }

    return render(request, "author_detail.html", context)