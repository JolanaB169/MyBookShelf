from django.shortcuts import redirect, Http404
from books.services.importers.google_importer import import_book_from_google


def import_book_view(request, source, external_id):
    """
    Import a book from an external source (Google Books or OpenLibrary)
    and redirect to its detail page.

    Args:
        request: Django request object
        source: "google" or "openlibrary"
        external_id: External ID of the book

    Returns:
        Redirects to the detail page of the imported book.
    """
    if source == "google":
        book = import_book_from_google(external_id)

    else:
        raise Http404("Unknown source")

    # book is already a Book instance
    return redirect("book_detail", book_id=book.id)
