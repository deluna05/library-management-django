from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("history/", views.borrow_history, name="borrow_history"),

    path("api/books/", views.api_books, name="api_books"),
    path("api/borrow/", views.api_borrow, name="api_borrow"),
]
