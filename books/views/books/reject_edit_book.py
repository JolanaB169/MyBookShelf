from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from books.models.books import Book

@staff_member_required
def reject_book_changes(request, book_id):
    """
    Rejects pending edits for a book without modifying the original data.
    """
    book = get_object_or_404(Book, id=book_id)

    if not book.pending_edit or not book.pending_data:
        messages.warning(request, "Žádné čekající změny k zamítnutí.")
        return redirect("book_detail", book_id=book.id)

    # Reject pending changes: clear pending_data, keep the original book unchanged
    book.pending_data = None
    book.pending_edit = False
    book.save()

    messages.info(request, "Navrhované změny byly zamítnuty.")
    return redirect("pending_edits")
