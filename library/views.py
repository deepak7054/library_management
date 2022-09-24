from datetime import datetime

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Students, Book, BookIssue
from library.serializer import AddStudentSerializer, AddBookSerializer, BorrowBookSerializer, RenewBookSerializer, \
    ReturnBookSerializer, ResponseBookSerializer, BorrowedBookSerializer, StudentBorrowedHistorySerializer
from library.utility import returnDate

import pytz
utc=pytz.UTC


class AddStudent(APIView):
    def post(self, request):
        try:
            ser = AddStudentSerializer(data=request.data)
            if ser.is_valid():
                Students.objects.create(**ser.data)
                return Response("Student Created Successfully!!", status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "Student Creation Failed!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            student = Students.objects.filter(roll_number=request.data.get('roll_number')).first()
            if student:
                ser = AddStudentSerializer(student)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                students = Students.objects.all()
                ser = AddStudentSerializer(students, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "Some error found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddBooks(APIView):
    def post(self, request):
        try:
            ser = AddBookSerializer(data=request.data, many=True)
            if ser.is_valid():
                for data in ser.initial_data:
                    Book.objects.create(**data)
                return Response("Book Created Successfully!!", status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "Books Creation Failed!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            book_obj = Book.objects.filter(id=request.data.get('book_id')).first()
            if book_obj:
                ser = ResponseBookSerializer(book_obj)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                book_obj = Book.objects.all()
                ser = ResponseBookSerializer(book_obj, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "getting some error!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BorrowBook(APIView):
    def post(self, request):
        try:
            ser = BorrowBookSerializer(data=request.data)
            if ser.is_valid():
                book_id = ser.validated_data.get('book_id')
                student_id = ser.validated_data.get('student_id')
                book_obj = Book.objects.filter(id=book_id).first()
                student_obj = Students.objects.filter(id=student_id).first()
                if book_obj and student_obj:
                    if book_obj.stock > 0:
                        if student_obj.borrowed_books < 10:
                            book_issue, created = BookIssue.objects.get_or_create(student=student_obj, book=book_obj, is_returned=False)
                            if created:
                                student_obj.borrowed_books += 1
                                book_obj.stock -= 1
                                student_obj.save()
                                book_obj.save()
                                return Response("Student borrowed 1 book successfully!!", status=status.HTTP_201_CREATED)
                            return Response("Student already borrowed this book",
                                            status=status.HTTP_200_OK)
                        return Response("Student already borrowed 10 books!!", status=status.HTTP_200_OK)
                    return Response("No stock available of this book!!", status=status.HTTP_200_OK)
                return Response("Book or student not found!!", status=status.HTTP_400_BAD_REQUEST)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "Borrow book Failed!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RenewBook(APIView):
    def post(self, request):
        try:
            ser = RenewBookSerializer(data=request.data)
            if ser.is_valid():
                book_id = ser.validated_data.get('book_id')
                student_id = ser.validated_data.get('student_id')
                book_obj = Book.objects.filter(id=book_id).first()
                student_obj = Students.objects.filter(id=student_id).first()
                if book_obj and student_obj:
                    borrowed = BookIssue.objects.filter(student=student_id, book=book_id, is_returned=False).latest('id')
                    if borrowed:
                        if not borrowed.is_renewed:
                            if utc.localize(datetime.now()) < borrowed.due_date:
                                borrowed.is_renewed = True
                                borrowed.due_date = returnDate()
                                borrowed.save()
                                return Response("Renew Book successfully", status=status.HTTP_201_CREATED)
                            return Response("You crossed the due date", status=status.HTTP_200_OK)
                        return Response("this is already renewed", status=status.HTTP_200_OK)
                    return Response("No issue book found", status=status.HTTP_400_BAD_REQUEST)
                return Response("Book or student not found!!", status=status.HTTP_400_BAD_REQUEST)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "Renew book Failed!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReturnBook(APIView):
    def post(self, request):
        try:
            ser = ReturnBookSerializer(data=request.data)
            if ser.is_valid():
                book_id = ser.validated_data.get('book_id')
                student_id = ser.validated_data.get('student_id')
                book_obj = Book.objects.filter(id=book_id).first()
                student_obj = Students.objects.filter(id=student_id).first()
                if book_obj and student_obj:
                    borrowed = BookIssue.objects.filter(student=student_id, book=book_id, is_returned=False).latest('id')
                    if borrowed:
                        borrowed.returned_date = datetime.today()
                        borrowed.is_returned = True
                        borrowed.save()
                        book_obj.stock += 1
                        book_obj.save()
                        student_obj.borrowed_books -= 1
                        student_obj.save()
                        return Response("Book return successfully", status=status.HTTP_201_CREATED)
                    return Response("No issue book found", status=status.HTTP_400_BAD_REQUEST)
                return Response("Book or student not found!!", status=status.HTTP_400_BAD_REQUEST)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "Book Return Failed!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentBorrowedBook(APIView):
    def get(self, request):
        try:
            book_issue = BookIssue.objects.filter(student=request.data.get('student_id'), is_returned=False)
            if book_issue:
                ser = BorrowedBookSerializer(book_issue, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            return Response("No borrowed book found!!", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "getting some error!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentBorrowedHistory(APIView):
    def get(self, request):
        try:
            book_issue = BookIssue.objects.filter(student=request.data.get('student_id'))
            if book_issue:
                ser = StudentBorrowedHistorySerializer(book_issue, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            return Response("No History found!!", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"msg": "getting some error!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


