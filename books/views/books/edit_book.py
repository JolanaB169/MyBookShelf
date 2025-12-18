from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from books.forms import BookForm
from books.models.books import Book, Author

@login_required
def edit_book_view(request, book_id):
    """
    View for editing a book.

    - Admins can save changes directly.
    - Regular users can propose changes; these are saved to pending_data
      and require admin approval.
    """
    book = get_object_or_404(Book, id=book_id)
    user_is_admin = request.user.is_staff or request.user.is_superuser

    # --- Initialize form ---
    if request.method == "POST":
        # Admin uses instance to save directly; users only for validation
        form = BookForm(request.POST, request.FILES, instance=book if user_is_admin else None)
    else:
        if user_is_admin:
            form = BookForm(instance=book)
        else:
            # Regular user: show current values as initial
            initial_data = {
                "title": book.title,
                "isbn": book.isbn,
                "publisher": book.publisher,
                "pages": book.pages,
                "year": book.year,
                "description": book.description,
                "genre": book.genre.all(),
                "new_authors": "",  # empty field for proposing authors
            }
            form = BookForm(initial=initial_data)

    if request.method == "POST" and form.is_valid():
        proposed_data = {}

        for field, value in form.cleaned_data.items():
            # Skip helper fields
            if field == "existing_authors":
                continue

            # Process new authors
            if field == "new_authors" and value:
                new_authors = []
                for full_name in value.split("\n"):
                    full_name = full_name.strip()
                    if not full_name:
                        continue
                    parts = full_name.split(" ", 1)
                    first_name = parts[0]
                    last_name = parts[1] if len(parts) > 1 else ""
                    author, _ = Author.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        defaults={"year_of_birth": 1900}
                    )
                    new_authors.append(author)
                proposed_data["new_authors"] = [a.id for a in new_authors]
                continue

            # Process ManyToMany fields
            if hasattr(value, "all"):
                proposed_data[field] = [obj.id for obj in value.all()]
            else:
                proposed_data[field] = value

        if user_is_admin:
            # Admin: save changes directly
            for field, value in proposed_data.items():
                if field == "new_authors":
                    book.authors.add(*Author.objects.filter(id__in=value))
                    continue

                if hasattr(book, field):
                    field_obj = Book._meta.get_field(field)
                    if field_obj.many_to_many:
                        related_model = field_obj.related_model
                        getattr(book, field).set(related_model.objects.filter(id__in=value))
                    else:
                        setattr(book, field, value)
            book.pending_edit = False
            book.pending_data = None
            book.save()
            messages.success(request, "Změny byly uloženy.")
        else:
            # Regular user: save pending_data only
            book.pending_data = proposed_data
            book.pending_edit = True
            if not book.created_by:
                book.created_by = request.user
            book.edit_proposed_by = request.user
            book.save()
            messages.info(request, "Změny byly odeslány ke schválení.")

        return redirect("book_detail", book_id=book.id)

    return render(request, "books/edit_book.html", {"form": form, "book": book})