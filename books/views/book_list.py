
from django.shortcuts import render
from ..models import Book, Genre, Author

def book_list_view(request):
    """Displays a list of books with optional filtering by title, genre, author, and year."""
    books = Book.objects.all()

    title = request.GET.get("title")
    genre = request.GET.get("genre")
    author = request.GET.get("author")
    year = request.GET.get("year")

    if title:
        books = books.filter(title__icontains=title)

    if genre:
        books = books.filter(genre__id=genre)

    if author:
        books = books.filter(authors__id=author)

    if year:
        books = books.filter(year=year)

    context = {
        "books": books.distinct(),
        "genres": Genre.objects.all(),
        "authors": Author.objects.all()
    }

    return render(request, "book_list.html", context)
