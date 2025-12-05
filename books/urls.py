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
    path('author/<int:author_id>/favorite/', favorite_author, name='favorite_author'),
    path("genre-search/", genre_search_view, name="genre_search"),


]