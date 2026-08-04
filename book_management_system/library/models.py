from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Book(models.Model):
    """Represents a book title held by the library, along with stock counts."""

    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('Mathematics', 'Mathematics'),
        ('Computer Science', 'Computer Science'),
        ('Engineering', 'Engineering'),
        ('History', 'History'),
        ('Biography', 'Biography'),
        ('Reference', 'Reference'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r'^\d{10}(\d{3})?$', 'Enter a valid 10 or 13 digit ISBN.')],
        help_text='10 or 13 digit ISBN number'
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    publisher = models.CharField(max_length=255, blank=True)
    publication_year = models.PositiveIntegerField(validators=[MinValueValidator(1500)])
    quantity = models.PositiveIntegerField(default=1, help_text='Total number of copies owned by the library')
    available_quantity = models.PositiveIntegerField(default=1, help_text='Number of copies currently available to issue')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def is_available(self):
        return self.available_quantity > 0

    def clean(self):
        # Guard against available_quantity ever exceeding total quantity.
        if self.available_quantity is not None and self.quantity is not None:
            if self.available_quantity > self.quantity:
                raise ValidationError('Available quantity cannot exceed total quantity.')


class Student(models.Model):
    """Represents a library member (student) who can borrow books."""

    DEPARTMENT_CHOICES = [
        ('MCA', 'MCA'),
        ('MSc CS', 'M.Sc Computer Science'),
        ('MSc IT', 'M.Sc Information Technology'),
        ('BSc CS', 'B.Sc Computer Science'),
        ('BCA', 'BCA'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    register_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='MSc CS')
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10 digit phone number.')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.register_number})"

    def active_borrow_count(self):
        return self.borrow_set.filter(status='Issued').count()


class Borrow(models.Model):
    """Represents a single issue/return transaction linking a Student and a Book."""

    STATUS_CHOICES = [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Issued')

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.book.title} -> {self.student.name} [{self.status}]"

    def is_overdue(self):
        """A book is considered overdue if issued more than 14 days ago and not yet returned."""
        if self.status == 'Issued':
            due = self.issue_date + timezone.timedelta(days=14)
            return timezone.now().date() > due
        return False
