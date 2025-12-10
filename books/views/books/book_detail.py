from django.shortcuts import get_object_or_404, render, redirect
from books.models.books import Book


def book_detail_view(request, book_id):
    """
    Display a book detail page, handle image upload,
    and provide user's booklists with information if the book is already added.
    """
    book = get_object_or_404(Book, id=book_id)

    # Handle image upload
    if request.method == 'POST' and 'image' in request.FILES:
        book.image = request.FILES['image']
        book.save()
        return redirect("book_detail", book_id=book_id)

    # Prepare user's booklists for template
    user_booklists = []
    if request.user.is_authenticated:
        for bl in request.user.booklists.all():
            # Get IDs of books already in this list
            book_ids = list(bl.items.values_list('book_id', flat=True))
            user_booklists.append({'list': bl, 'book_ids': book_ids})

    context = {
        "book": book,
        "user_booklists": user_booklists,
    }

    return render(request, "books/book_detail.html", context)
