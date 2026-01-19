from django.contrib import admin
from .models import Category, Book, BorrowRecord


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "year", "available")
    search_fields = ("title", "author", "isbn")
    list_filter = ("available", "category", "year")
    list_select_related = ("category",)


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "book", "borrowed_at", "due_at", "returned_at", "is_overdue")
    search_fields = ("user__username", "book__title", "book__author")
    list_filter = ("returned_at", "due_at", "borrowed_at")
    list_select_related = ("user", "book")
