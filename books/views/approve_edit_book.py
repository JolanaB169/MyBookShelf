from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from ..models.books import Book, Author


@staff_member_required
def approve_book_changes(request, book_id):
    """
    Approves pending edits for a book submitted by users.
    """
    book = get_object_or_404(Book, id=book_id)

    # Check if there are pending edits
    if not book.pending_edit or not book.pending_data:
        messages.warning(request, "Žádné změny čekající na schválení.")
        return redirect("book_detail", book_id=book.id)

    data = book.pending_data

    # --- 1) Apply standard fields from pending_data ---
    for field, value in data.items():

        # Skip helper fields from the form
        if field in ["existing_authors", "new_authors"]:
            continue

        # Skip fields not actually on the model
        if not hasattr(book, field):
            continue

        field_obj = Book._meta.get_field(field)

        # Handle ManyToMany fields (e.g., genre)
        if field_obj.many_to_many:
            related_model = field_obj.related_model
            getattr(book, field).set(related_model.objects.filter(id__in=value))
        else:
            setattr(book, field, value)

    # --- 2) Process existing authors ---
    existing_authors = data.get("existing_authors")
    new_authors_text = data.get("new_authors", "").strip()

    all_author_ids = []

    if existing_authors:
        all_author_ids.extend(existing_authors)

    # --- 3) Create new authors from new_authors field ---
    if new_authors_text:
        for line in new_authors_text.split("\n"):
            full_name = line.strip()
            if not full_name:
                continue

            parts = full_name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

            author, created = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                defaults={"year_of_birth": 1900}  # placeholder
            )
            all_author_ids.append(author.id)

    # --- 4) Save authors to the book ---
    if all_author_ids:
        book.authors.set(Author.objects.filter(id__in=all_author_ids))

    # --- 5) Complete approval ---
    book.pending_data = None
    book.pending_edit = False
    book.approved = True
    book.save()

    messages.success(request, "Čekající změny byly úspěšně schváleny.")
    return redirect("pending_edits")
