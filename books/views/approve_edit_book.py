from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from ..models.books import Book

@staff_member_required
def approve_book_changes(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.pending_edit or not book.pending_data:
        messages.warning(request, "Žádné čekající změny k potvrzení.")
        return redirect("book_detail", book_id=book.id)

    data = book.pending_data

    for field, value in data.items():
        field_obj = Book._meta.get_field(field)

        if field_obj.many_to_many:
            related_model = field_obj.related_model
            getattr(book, field).set(related_model.objects.filter(id__in=value))
        else:
            setattr(book, field, value)

    book.pending_data = None
    book.pending_edit = False
    book.save()

    messages.success(request, "Změny byly úspěšně schváleny.")
    return redirect("pending_edits")
