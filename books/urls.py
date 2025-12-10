from django.urls import path
from .views.home import home_page

# Books
from books.views.books.search_books_view import search_books_view
from books.views.books.book_detail import book_detail_view
from books.views.books.edit_book import edit_book_view
from books.views.books.add_book import add_book_view
from books.views.books.approve_edit_book import approve_book_changes
from books.views.books.reject_edit_book import reject_book_changes
from books.views.books.pending_edit_book import pending_edits_view

# Authors
from books.views.authors.author_detail import author_detail_view
from books.views.authors.search_author import search_author_view
from books.views.authors.edit_author import edit_author_view
from books.views.authors.add_author import add_author_view
from books.views.authors.favourite_author import favorite_author

# Users
from books.views.users.login import login_view
from books.views.users.logout import logout_view
from books.views.users.register import register_view
from books.views.users.profile import profile_view

# Genres
from books.views.genre.genre_search import genre_search_view
from books.views.genre.genre_books import genre_books_view

# Booklists
from books.views.booklist.book_list import book_list_view
from books.views.booklist.create_booklist import create_booklist
from books.views.booklist.booklist_detail import booklist_detail
from books.views.booklist.add_book_to_lists import add_book_to_lists
from books.views.booklist.remove_book_from_list import remove_book_from_list


urlpatterns = [
    path('', home_page, name='home_page'),

    # --- Books ---
    path("search/", search_books_view, name="book_search"),
    path('book/<int:book_id>/', book_detail_view, name='book_detail'),
    path('edit_book/<int:book_id>/edit/', edit_book_view, name='edit_book'),
    path('add_book/', add_book_view, name='add_book_view'),
    path('book/<int:book_id>/approve/', approve_book_changes, name='approve_edit_book'),
    path('book/<int:book_id>/reject/', reject_book_changes, name='reject_edit_book'),
    path('books/pending-edits/', pending_edits_view, name='pending_edits'),

    # --- Authors ---
    path('author/<str:author_name>/', author_detail_view, name='author_detail'),
    path('author-search/', search_author_view, name='author_search'),
    path('edit_author/<int:author_id>/edit/', edit_author_view, name='edit_author'),
    path('authors/add/', add_author_view, name='add_author'),
    path('favourite_author/<int:author_id>/favorite/', favorite_author, name='favorite_author'),

    # --- Users ---
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),

    # --- Genres ---
    path("genre-search/", genre_search_view, name="genre_search"),
    path("genre/<int:genre_id>/books/", genre_books_view, name="genre_books"),

    # --- Booklists ---
    path("books/", book_list_view, name="book_list"),
    path("booklist/create/", create_booklist, name="create_booklist"),
    path('booklist/<int:list_id>/', booklist_detail, name="booklist_detail"),
    path('book/<int:book_id>/add_to_lists/', add_book_to_lists, name='add_book_to_lists'),
    path("booklist/<int:list_id>/remove/<int:book_id>/", remove_book_from_list, name="remove_book_from_list"),
]
