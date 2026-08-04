from django.contrib import admin
from .models import Book, Student, Borrow


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'available_quantity', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'register_number', 'department', 'email', 'phone')
    search_fields = ('name', 'register_number', 'email')
    list_filter = ('department',)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issue_date', 'return_date', 'status')
    list_filter = ('status',)
    search_fields = ('book__title', 'student__name')
