from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from books.models.books import Book
from books.models.booklist import BookList, BookListItem

@login_required
def add_book_to_lists(request, book_id):
    """
    Add a book to one or more of the logged-in user's booklists.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        list_ids = request.POST.getlist("booklists")  # get multiple selected lists
        if not list_ids:
            messages.warning(request, "Musíte vybrat alespoň jeden seznam.")
            return redirect("book_detail", book_id=book.id)

        added_count = 0
        for list_id in list_ids:
            booklist = get_object_or_404(BookList, id=list_id, owner=request.user)

            obj, created = BookListItem.objects.get_or_create(booklist=booklist, book=book)
            if created:
                added_count += 1

        if added_count:
            messages.success(request, f"Kniha byla přidána do {added_count} seznamů.")
        else:
            messages.info(request, "Kniha byla již ve vybraných seznamech.")

    return redirect("books/book_detail", book_id=book.id)
