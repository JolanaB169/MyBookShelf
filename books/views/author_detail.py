# books/views/author_detail.py
from django.shortcuts import render, get_object_or_404
from books.models import Book, Author
from books.services.google_books import search_google_books
from books.services.wiki_author import get_author_bio


def author_detail_view(request, author_name):
    """
    View for displaying all books by a specific author from your DB,
    with suggestions from Google Books and Open Library.
    """
    # --- Rozdělení jména autora ---
    parts = author_name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    # --- 1) Books from your database ---
    db_books = Book.objects.filter(
        authors__first_name__iexact=first_name,
        authors__last_name__iexact=last_name
    )

    # --- 2) Google Books suggestions ---
    google_books = []
    try:
        for item in search_google_books(author_name):
            info = item.get("volumeInfo", {})
            authors = info.get("authors", [])
            if author_name in authors:
                google_books.append({
                    "title": info.get("title", "Untitled"),
                    "external_id": item.get("id"),
                    "source": "google",
                    "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
                })
    except Exception:
        google_books = []  # pokud Google Books API spadne, nic se nestane


    # --- 4) Wikipedia bio ---
    author_bio = get_author_bio(author_name)

    context = {
        "author_name": author_name,
        "db_books": db_books,
        "google_books": google_books,
        "author_bio": author_bio
    }

    return render(request, "author_detail.html", context)
