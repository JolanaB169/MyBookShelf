from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from books.models.booklist import BookList, BookListItem

@login_required
def remove_book_from_list(request, list_id, book_id):
    """
    Remove a book from a specific booklist owned by the logged-in user.
    """
    booklist = get_object_or_404(BookList, id=list_id, owner=request.user)
    item = get_object_or_404(BookListItem, booklist=booklist, book_id=book_id)

    item.delete()
    messages.success(request, "Kniha byla odebrána ze seznamu.")
    return redirect("booklist_detail", list_id=list_id)
