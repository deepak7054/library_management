from django.urls import path
from library.views import AddStudent, AddBooks, BorrowBook, StudentBorrowedBook, RenewBook, ReturnBook, \
    StudentBorrowedHistory

# region library management API URLs
urlpatterns = [
    path('add_student/', AddStudent.as_view(), name='add-student'),
    path('add_books/', AddBooks.as_view(), name='add-books'),
    path('book_borrow/', BorrowBook.as_view(), name='book-issue'),
    path('renew_book/', RenewBook.as_view(), name='renew-book'),
    path('return_book/', ReturnBook.as_view(), name='return-book'),
    path('student_borrowed_book/', StudentBorrowedBook.as_view(), name='borrowed-book'),
    path('borrowed_history/', StudentBorrowedHistory.as_view(), name='borrowed-history'),
]
# endregion
