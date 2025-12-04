from django.shortcuts import render
from books.services.google_books import get_google_book, search_google_books

def google_book_detail(request, volume_id):
    """
    View for displaying the detail of a single Google Books book.

    Args:
        request (HttpRequest): The Django request object.
        volume_id (str): The unique Google Books volume ID for the book.

    Returns:
        HttpResponse: Renders the book_detail.html template with book details
                      and other books by the same author.
    """
    # Fetch book details from Google Books API
    volume = get_google_book(volume_id)
    volume_info = volume.get("volumeInfo", {})

    title = volume_info.get("title", "Untitled")
    authors = volume_info.get("authors", [])
    description = volume_info.get("description", "No description available.")

    # Find other books by the same author
    author_books = []
    if authors:
        author_query = authors[0]  # use the first author for searching
        items = search_google_books(author_query)
        for item in items:
            b_info = item.get("volumeInfo", {})
            b_id = item.get("id")
            b_title = b_info.get("title", "Untitled")
            if b_id and b_id != volume_id:  # avoid including the current book
                author_books.append({"id": b_id, "title": b_title})

    context = {
        "volume": volume_info,
        "authors": authors,
        "description": description,
        "author_books": author_books,
        "current_volume_id": volume_id,
    }

    return render(request, "book_detail.html", context)