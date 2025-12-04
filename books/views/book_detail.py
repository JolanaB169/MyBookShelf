from django.shortcuts import get_object_or_404, render, Http404
from books.models.books import Book
import requests


def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {"book": book})