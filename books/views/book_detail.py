from django.shortcuts import get_object_or_404, render, Http404
from books.models.books import Book
from books.services.google_books import get_google_book
import requests


def book_detail_view(request, book_id):
    """
    book_id může být:
    - interní ID (int)
    - google_id
    - openlibrary_key
    """
    book = None

    # 1) interní DB
    if book_id.isdigit():
        book = get_object_or_404(Book, id=int(book_id))
        return render(request, "book_detail.html", {"book": book})

    # 2) externí Google Books
    try:
        book_data = get_google_book(book_id)
        volume_info = book_data.get("volumeInfo", {})
        if not volume_info:
            raise Http404("Book not found on Google Books")
        book = {
            "title": volume_info.get("title", "Untitled"),
            "authors": volume_info.get("authors", []),
            "description": volume_info.get("description", "No description available."),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
            "source": "google",
            "external_id": book_id,
        }
        return render(request, "book_detail.html", {"book": book})

    except requests.HTTPError as e:
        # Pokud API neodpoví nebo volume_id neexistuje
        raise Http404(f"Book not found on Google Books ({e.response.status_code})")
    except Exception as e:
        # jiné chyby
        raise Http404(f"Book not found: {str(e)}")