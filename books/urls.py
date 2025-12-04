from django.urls import path
from .views.home import home_page
from .views.search_books_view import search_books_view
from .views.book_detail import google_book_detail
from .views.author_detail import author_detail_view
from .views.search_author import search_author_view


urlpatterns = [
    path('', home_page, name='home_page'),
    path("search/", search_books_view, name="book_search"),
    path('book/<str:volume_id>/', google_book_detail, name='book_detail'),
    path('author/<str:author_name>/', author_detail_view, name='author_detail'),
    path('author-search/', search_author_view, name='author_search'),
]