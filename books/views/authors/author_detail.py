from django.shortcuts import render, get_object_or_404, redirect
from books.models import Author

def author_detail_view(request, author_name):
    """
    Display an author and their books from the database.
    Allows uploading a photo for the author.
    """

    parts = author_name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    author = get_object_or_404(Author, first_name__iexact=first_name, last_name__iexact=last_name)

    if request.method == "POST":
        photo = request.FILES.get("photo")
        if photo:
            author.photo = photo
            author.save()
        return redirect("author_detail", author_name=author_name)

    db_books = author.books.all()

    context = {
        "author": author,
        "db_books": db_books,
    }

    return render(request, "authors/author_detail.html", context)
