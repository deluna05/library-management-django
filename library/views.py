# API view to retrieve all books

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BorrowRecord
import json


def book_list(request):
    books = Book.objects.select_related("category").all().order_by("title")
    return render(request, "library/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = get_object_or_404(Book.objects.select_related("category"), id=book_id)
    return render(request, "library/book_detail.html", {"book": book})


@login_required
def borrow_history(request):
    records = BorrowRecord.objects.select_related("book", "user").filter(user=request.user)
    return render(request, "library/borrow_history.html", {"records": records})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from .models import Book, BorrowRecord


@csrf_exempt
def api_books(request):
    if request.method == "GET":
        books = Book.objects.select_related("category").all()
        data = []
        for b in books:
            data.append({
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "year": b.year,
                "isbn": b.isbn,
                "category": b.category.name if b.category else None,
                "available": b.available
            })
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        book = Book.objects.create(
            title=body.get("title"),
            author=body.get("author"),
            year=body.get("year"),
            isbn=body.get("isbn"),
        )
        return JsonResponse({"id": book.id, "message": "Book created"}, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_borrow(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = json.loads(request.body.decode("utf-8"))
    user_id = body.get("user_id")
    book_id = body.get("book_id")

    if not user_id or not book_id:
        return JsonResponse({"error": "user_id and book_id are required"}, status=400)

    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)

    try:
        record = BorrowRecord.borrow_book(user=user, book=book, days=14)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "message": "Book borrowed",
        "borrow_id": record.id,
        "due_at": record.due_at
    }, status=201)

@csrf_exempt
def api_book_detail(request, book_id):

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "PUT":
        body = json.loads(request.body.decode("utf-8"))

        book.title = body.get("title", book.title)
        book.author = body.get("author", book.author)
        book.year = body.get("year", book.year)
        book.isbn = body.get("isbn", book.isbn)
        book.save()

        return JsonResponse({"message": "Book updated"})

    if request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Book deleted"}, status=204)

    return JsonResponse({"error": "Method not allowed"}, status=405)
