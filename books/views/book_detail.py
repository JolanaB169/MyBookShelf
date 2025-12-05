from django.shortcuts import get_object_or_404, render, redirect
from books.models.books import Book



def book_detail_view(request, book_id):
    """Display a book detail page and handle image upload for the book."""

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            book.image = image
            book.save()
        return redirect("book_detail", book_id=book_id)

    return render(request, "book_detail.html", {"book": book})