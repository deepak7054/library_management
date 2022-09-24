from django.contrib import admin

# Register your models here.
from library.models import Students, Book, BookIssue

admin.site.register(Students)
admin.site.register(BookIssue)
admin.site.register(Book)