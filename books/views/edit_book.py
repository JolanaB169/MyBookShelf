from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import BookForm
from ..models.books import Book

@login_required
def edit_book_view(request, book_id):
    """
    Allow logged-in users to edit book details.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, "edit_book.html", {"form": form, "book": book})
