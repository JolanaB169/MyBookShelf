from django.contrib import admin
from .models import Author, Genre, Book
from .models.booklist import BookListItem, BookList

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookListItem)
admin.site.register(BookList)