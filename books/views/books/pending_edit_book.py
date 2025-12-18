from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from books.models.books import Book

@staff_member_required
def pending_edits_view(request):
    """Displays all books with pending edits."""
    books = Book.objects.filter(pending_edit=True).select_related("edit_proposed_by")
    return render(request, "books/pending_edits_book.html", {"books": books})