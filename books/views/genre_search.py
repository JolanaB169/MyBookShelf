from django.shortcuts import render
from books.models.genre import Genre
from books.models.books import Book

def genre_search_view(request):
    """
    Allows users to select a genre from a dropdown and shows books for that genre.
    """
    genres = Genre.objects.all()
    selected_genre = None
    books = None

    if request.method == "GET" and "genre_id" in request.GET:
        genre_id = request.GET.get("genre_id")
        try:
            selected_genre = Genre.objects.get(id=genre_id)
            books = Book.objects.filter(genre=selected_genre)
        except Genre.DoesNotExist:
            selected_genre = None
            books = None

    context = {
        "genres": genres,
        "selected_genre": selected_genre,
        "books": books,
    }
    return render(request, "genre_search.html", context)
