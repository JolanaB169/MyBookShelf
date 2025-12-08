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
    - Users can add new authors on the fly.
    - The user who proposes edits is recorded in `created_by` if not already set.
    """
    book = get_object_or_404(Book, id=book_id)
    user_is_admin = request.user.is_staff or request.user.is_superuser

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            # Handle new authors
            new_authors_raw = form.cleaned_data.get("new_authors", "")
            if new_authors_raw:
                from ..models.books import Author
                new_authors = []
                for full_name in new_authors_raw.split(","):
                    full_name = full_name.strip()
                    if not full_name:
                        continue
                    parts = full_name.split(" ", 1)
                    first_name = parts[0]
                    last_name = parts[1] if len(parts) > 1 else ""
                    author, created = Author.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        defaults={"year_of_birth": 1900}  # placeholder year, must satisfy non-null
                    )
                    new_authors.append(author)
                # Add new authors to the book
                form.instance.authors.add(*new_authors)

            if user_is_admin:
                # Admin can save changes directly
                form.save()
                book.pending_edit = False
                book.pending_data = None
                book.save()
                messages.success(request, "Book has been edited and changes approved.")
                return redirect("edit_book", book_id=book.id)  # stay on edit page
            else:
                # Regular user proposes edits
                proposed_data = {}
                for field, value in form.cleaned_data.items():
                    if hasattr(value, "all"):  # ManyToMany fields
                        proposed_data[field] = [obj.id for obj in value.all()]
                    else:
                        proposed_data[field] = value

                book.pending_data = proposed_data
                book.pending_edit = True

                if not book.created_by:
                    book.created_by = request.user

                book.save()
                messages.info(request, "Your proposed edits have been submitted for approval.")
                return redirect("book_detail", book_id=book.id)  # stay on edit page
    else:
        form = BookForm(instance=book)

    return render(request, "edit_book.html", {"form": form, "book": book})
