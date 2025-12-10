from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from books.models.books import Book
from books.models.booklist import BookList, BookListItem

@login_required
def booklist_detail(request, list_id):
    """
    Display a user's booklist and allow adding/removing books.
    """
    booklist = get_object_or_404(BookList, id=list_id, owner=request.user)
    all_books = Book.objects.all() # or filter by available books

    if request.method == "POST":
        book_id = request.POST.get("book_id")
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            # Add a book to the list if it is not already there
            item, created = BookListItem.objects.get_or_create(booklist=booklist, book=book)
            if created:
                messages.success(request, f"Kniha '{book.title}' byla přidána do seznamu.")
            else:
                messages.info(request, f"Kniha '{book.title}' je už v seznamu.")
            return redirect("booklist_detail", list_id=booklist.id)

    return render(request, "booklist/booklist_detail.html", {"booklist": booklist, "all_books": all_books})
