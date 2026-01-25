# books/urls.py
from django.urls import path
from .views import books_view, books_by_date_view

urlpatterns = [
    path('', books_view, name='books'),
    path('<str:pub_date>/', books_by_date_view, name='books_by_date'),
]