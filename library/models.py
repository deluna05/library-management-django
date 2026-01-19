from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books"
    )

    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


class BorrowRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="borrow_records"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_records"
    )

    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-borrowed_at"]

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    @property
    def is_returned(self):
        return self.returned_at is not None

    @property
    def is_overdue(self):
        if self.returned_at is not None:
            return False
        return timezone.now() > self.due_at

    def mark_returned(self):
        """
        Помечает книгу как возвращённую и делает book.available = True
        """
        if self.returned_at is None:
            self.returned_at = timezone.now()
            self.book.available = True
            self.book.save()
            self.save()

    @staticmethod
    def borrow_book(user, book, days=14):
        """
        Создаёт запись выдачи: ставит дедлайн (due_at) и делает книгу недоступной.
        """
        if not book.available:
            raise ValueError("Book is not available")

        book.available = False
        book.save()

        return BorrowRecord.objects.create(
            user=user,
            book=book,
            due_at=timezone.now() + timedelta(days=days)
        )
