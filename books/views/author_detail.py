from django.shortcuts import render, get_object_or_404
from ..models import Book, Author

def author_detail_view(request, author_name):
    """
    Zobrazuje autora a jeho knihy z vlastní DB.
    author_name = "Jméno Příjmení"
    """
    # Rozdělení jména
    parts = author_name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    # Najdi autora v DB, nebo 404
    author = get_object_or_404(Author, first_name__iexact=first_name, last_name__iexact=last_name)

    # Načti jeho knihy (už jde přes related_name 'books')
    db_books = author.books.all()

    context = {
        "author": author,
        "db_books": db_books,
    }

    return render(request, "author_detail.html", context)
