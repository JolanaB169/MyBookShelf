from django.urls import path
from .views.home import home_page
# from .views.books import book_list, book_detail
# from .views.authors import author_detail, author_list

urlpatterns = [
    path('', home_page, name='home_page'),
    # path('books/', book_list, name='book_list'),
    # path('book/<int:pk>/', book_detail, name='book_detail'),
    # path('author/<int:pk>/', author_detail, name='author_detail'),
    # path('authors/', author_list, name='author_list'),


]