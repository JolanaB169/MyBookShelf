from django.shortcuts import render, get_object_or_404, redirect
from books.models import Author

def author_detail_view(request, pk):
    """
    Display an author and their books from the database.
    Allows uploading a photo for the author.
    """

    author = get_object_or_404(Author, pk=pk)

    if request.method == "POST":
        photo = request.FILES.get("photo")
        if photo:
            author.photo = photo
            author.save()
        return redirect("author_detail", pk=author.pk)

    db_books = author.books.all()

    context = {
        "author": author,
        "db_books": db_books,
    }

    return render(request, "authors/author_detail.html", context)
