from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} — {self.author}"
from django.db import models

# Create your models here.
