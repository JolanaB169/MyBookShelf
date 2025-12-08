from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..forms import BookForm
from ..models.books import Book


@login_required
def edit_book_view(request, book_id):
    """
    View for editing an existing book.

    - Staff users can directly save changes, which automatically approves them.
    - Regular users submit proposed edits, which are stored in `pending_data` for approval.
    - The user who proposes edits is recorded in `created_by` if not already set.
    """
    book = get_object_or_404(Book, id=book_id)
    user_is_admin = request.user.is_staff or request.user.is_superuser

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            if user_is_admin:
                # Admin can save changes directly
                form.save()
                book.pending_edit = False
                book.pending_data = None
                book.save()
                messages.success(request, "Book has been edited and changes approved.")
                return redirect("book_detail", book_id=book.id)
            else:
                # Regular user proposes edits
                proposed_data = {}
                for field, value in form.cleaned_data.items():
                    if hasattr(value, "all"):  # Handle ManyToMany fields
                        proposed_data[field] = [obj.id for obj in value.all()]
                    else:
                        proposed_data[field] = value

                book.pending_data = proposed_data
                book.pending_edit = True

                # Record the user who proposed the edit
                if not book.created_by:
                    book.created_by = request.user

                book.save()
                messages.info(request, "Your proposed edits have been submitted for approval.")
                return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, "edit_book.html", {"form": form, "book": book})
