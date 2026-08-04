from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import Book, Student, Borrow
from .forms import LoginForm, BookForm, StudentForm, IssueBookForm, ReturnBookForm


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def login_view(request):
    """Handle admin login. Redirects to dashboard if already authenticated."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next')
                return redirect(next_url or 'dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user_obj': request.user})


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@login_required
def dashboard(request):
    total_books = Book.objects.count()
    available_books = sum(b.available_quantity for b in Book.objects.all())
    issued_books = Borrow.objects.filter(status='Issued').count()
    returned_books = Borrow.objects.filter(status='Returned').count()
    total_students = Student.objects.count()

    recent_activities = Borrow.objects.select_related('student', 'book').order_by('-issue_date')[:8]

    context = {
        'total_books': total_books,
        'available_books': available_books,
        'issued_books': issued_books,
        'returned_books': returned_books,
        'total_students': total_students,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard.html', context)


# ---------------------------------------------------------------------------
# Book Management
# ---------------------------------------------------------------------------

@login_required
def book_list(request):
    books = Book.objects.all()

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    author = request.GET.get('author', '').strip()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        books = books.filter(category=category)

    if author:
        books = books.filter(author__icontains=author)

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Book.CATEGORY_CHOICES
    authors = Book.objects.values_list('author', flat=True).distinct().order_by('author')

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'selected_author': author,
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'books.html', context)


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully.')
    return redirect('book_list')


# ---------------------------------------------------------------------------
# Student Management
# ---------------------------------------------------------------------------

@login_required
def student_list(request):
    students = Student.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(register_number__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query)
        )

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'students.html', context)


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form, 'student': student})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'Student "{name}" deleted successfully.')
    return redirect('student_list')


# ---------------------------------------------------------------------------
# Borrow / Return Module
# ---------------------------------------------------------------------------

@login_required
def borrow_list(request):
    return redirect('issue_book')


@login_required
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            # Double-check availability at the point of issue to prevent race conditions.
            if book.available_quantity <= 0:
                messages.error(request, f'"{book.title}" is currently unavailable and cannot be issued.')
            else:
                borrow = form.save(commit=False)
                borrow.issue_date = timezone.now().date()
                borrow.status = 'Issued'
                borrow.save()

                book.available_quantity -= 1
                book.save()

                messages.success(request, f'"{book.title}" issued to {borrow.student.name} successfully.')
                return redirect('issue_book')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = IssueBookForm()

    status_filter = request.GET.get('status', '').strip()
    borrows = Borrow.objects.select_related('student', 'book').all()
    if status_filter:
        borrows = borrows.filter(status=status_filter)

    paginator = Paginator(borrows, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'issue_book.html', {'form': form, 'page_obj': page_obj, 'selected_status': status_filter})


@login_required
def return_book(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)

    if borrow.status == 'Returned':
        messages.info(request, 'This book has already been returned.')
        return redirect('issue_book')

    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            borrow.status = 'Returned'
            borrow.return_date = timezone.now().date()
            borrow.save()

            book = borrow.book
            book.available_quantity += 1
            book.save()

            messages.success(request, f'"{book.title}" returned successfully by {borrow.student.name}.')
            return redirect('issue_book')
        else:
            messages.error(request, 'Please confirm the return to proceed.')
    else:
        form = ReturnBookForm()

    return render(request, 'return_book.html', {'form': form, 'borrow': borrow})


# ---------------------------------------------------------------------------
# Custom error views
# ---------------------------------------------------------------------------

def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def error_500_view(request):
    return render(request, '500.html', status=500)
