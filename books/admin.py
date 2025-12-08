from django.contrib import admin
from .models import Author, Book, BookList, BookListItem, Genre

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "year_of_birth", "year_of_death")
    search_fields = ("first_name", "last_name")
    list_filter = ("year_of_birth", "year_of_death", "country")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "year")
    search_fields = ("title", "authors__first_name", "authors__last_name")
    list_filter = ("year", "publisher")
    filter_horizontal = ("authors",)

@admin.register(BookList)
class BookListAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    search_fields = ("name", "owner__username")

@admin.register(BookListItem)
class BookListItemAdmin(admin.ModelAdmin):
    list_display = ("booklist", "book", "added_at")
    search_fields = ("booklist__name", "book__title")

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
