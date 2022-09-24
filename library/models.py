from django.db import models
from django.db import models
import uuid
from library.utility import returnDate
# Create your models here.


class Students(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    roll_number = models.CharField(max_length=100, unique=True)
    standard = models.CharField(max_length=100)
    borrowed_books = models.PositiveIntegerField(default=0, help_text="Quantity borrowed of books")

    def __str__(self):
        return self.first_name + ' ' + self.last_name if self.last_name else ''


class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, help_text="Description about the book", null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, help_text="Quantity available of this product")

    class Meta:
        unique_together = ('book_title', 'book_author')

    def __str__(self):
        return self.book_title


class BookIssue(models.Model):
    student = models.ForeignKey('Students', related_name='students', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', related_name='book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now=True, help_text="Book Issue Date")
    due_date = models.DateTimeField(default=returnDate(), help_text="Book Due date")
    returned_date = models.DateField(null=True, blank=True, help_text="Book Return Date")
    is_renewed = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)


