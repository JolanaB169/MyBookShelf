from django.shortcuts import render, redirect, get_object_or_404
from books.models.genre import Genre
from books.models.books import Book


def genre_books_view(request, genre_id):
    """
    Display all books of a selected genre.
    Logged-in users can add this genre to their profile favorites.
    """
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genre=genre)

    if request.method == "POST" and request.user.is_authenticated:

        action = request.POST.get("action")
        profile = request.user.profile

        if action == "add":
            profile.favorite_genres.add(genre)
        elif action == "remove":
            profile.favorite_genres.remove(genre)

        return redirect("genre_books", genre_id=genre.id)

    context = {
        "genre": genre,
        "books": books
    }
    return render(request, "genre_books.html", context)
