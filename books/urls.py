from django.urls import path
from .views.home import home_page
from .views.search_books_view import search_books_view
from .views.book_detail import book_detail_view
from .views.author_detail import author_detail_view
from .views.search_author import search_author_view
from .views.logout import logout_view
from .views.login import login_view
from .views.register import register_view
from .views.profile import profile_view
from .views.favourite_author import favorite_author
from .views.genre_search import genre_search_view
from .views.genre_books import genre_books_view
from .views.edit_book import edit_book_view
from .views.edit_author import edit_author_view
from .views.book_list import book_list_view
from .views.approve_edit_book import approve_book_changes
from .views.pending_edit_book import pending_edits_view
from .views.add_book import add_book_view
from .views.add_author import add_author_view
from .views.reject_edit_book import reject_book_changes



urlpatterns = [
    path('', home_page, name='home_page'),
    path("search/", search_books_view, name="book_search"),
    path('book/<str:book_id>/', book_detail_view, name='book_detail'),
    path('author/<str:author_name>/', author_detail_view, name='author_detail'),
    path('author-search/', search_author_view, name='author_search'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('favourite_author/<int:author_id>/favorite/', favorite_author, name='favorite_author'),
    path("genre-search/", genre_search_view, name="genre_search"),
    path("genre/<int:genre_id>/books/", genre_books_view, name="genre_books"),
    path('edit_book/<int:book_id>/edit/', edit_book_view, name='edit_book'),
    path('edit_author/<int:author_id>/edit/', edit_author_view, name='edit_author'),
    path("books/", book_list_view, name="book_list"),
    path('book/<int:book_id>/approve/', approve_book_changes, name='approve_edit_book'),
    path('books/pending-edits/', pending_edits_view, name='pending_edits'),
    path('add_book', add_book_view, name='add_book_view'),
    path('authors/add/', add_author_view, name='add_author'),
    path("book/<int:book_id>/reject/", reject_book_changes, name="reject_edit_book"),
]


