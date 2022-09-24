from rest_framework import serializers

from library.models import Students, Book, BookIssue


class AddStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ('first_name', 'last_name', 'roll_number', 'standard')


class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_title', 'book_author', 'stock', 'description')


class BorrowBookSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
    book_id = serializers.IntegerField(required=True)


class RenewBookSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
    book_id = serializers.IntegerField(required=True)


class ReturnBookSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
    book_id = serializers.IntegerField(required=True)


class ResponseBookSerializer(serializers.Serializer):
    bookTitle = serializers.SerializerMethodField('get_bookTitle')
    msg = serializers.SerializerMethodField('get_msg')
    description = serializers.SerializerMethodField('get_description')
    bookAuthor = serializers.SerializerMethodField('get_bookAuthor')

    def get_bookTitle(self, obj):
        return obj.book_title

    def get_description(self, obj):
        return obj.description

    def get_bookAuthor(self, obj):
        return obj.book_author

    def get_msg(self, obj):
        if obj.stock > 0:
            return "Total Available quantity " + str(obj.stock)
        else:
            book_issue = BookIssue.objects.filter(is_returned=False, book_id=obj.id).first()
            if book_issue:
                return "No stock available of this product. It will be available- " + book_issue.due_date
            else:
                return ''


class BorrowedBookSerializer(serializers.Serializer):
    bookTitle = serializers.SerializerMethodField('get_bookTitle')
    bookAuthor = serializers.SerializerMethodField('get_bookAuthor')
    IsRenewed = serializers.SerializerMethodField('get_IsRenewed')
    dueDate = serializers.SerializerMethodField('get_dueDate')

    def get_bookTitle(self, obj):
        return obj.book.book_title

    def get_bookAuthor(self, obj):
        return obj.book.book_author

    def get_IsRenewed(self, obj):
        return obj.is_renewed

    def get_dueDate(self, obj):
        return str(obj.due_date.day) + '-' + str(obj.due_date.month) + '-' + str(obj.due_date.year)


class StudentBorrowedHistorySerializer(serializers.Serializer):
    bookTitle = serializers.SerializerMethodField('get_bookTitle')
    bookAuthor = serializers.SerializerMethodField('get_bookAuthor')
    IsRenewed = serializers.SerializerMethodField('get_IsRenewed')
    returnedDate = serializers.SerializerMethodField('get_returnedDate')
    issueDate = serializers.SerializerMethodField('get_issueDate')
    dueDate = serializers.SerializerMethodField('get_dueDate')

    def get_bookTitle(self, obj):
        return obj.book.book_title

    def get_bookAuthor(self, obj):
        return obj.book.book_author

    def get_IsRenewed(self, obj):
        return obj.is_renewed

    def get_returnedDate(self, obj):
        return obj.returned_date if obj.returned_date else ''

    def get_issueDate(self, obj):
        return obj.issue_date

    def get_dueDate(self, obj):
        return str(obj.due_date.day) + '-' + str(obj.due_date.month) + '-' + str(obj.due_date.year)
