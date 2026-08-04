from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Book, Student, Borrow


class LoginForm(AuthenticationForm):
    """Custom-styled login form based on Django's built-in AuthenticationForm."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'})
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'publisher', 'publication_year', 'quantity', 'available_quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Author name'}),
            'isbn': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'ISBN (10 or 13 digits)'}),
            'category': forms.Select(attrs={'class': 'select-field'}),
            'publisher': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Publisher'}),
            'publication_year': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'e.g. 2023'}),
            'quantity': forms.NumberInput(attrs={'class': 'input-field', 'min': 0}),
            'available_quantity': forms.NumberInput(attrs={'class': 'input-field', 'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        available_quantity = cleaned_data.get('available_quantity')
        if quantity is not None and available_quantity is not None:
            if available_quantity > quantity:
                raise forms.ValidationError('Available quantity cannot be greater than total quantity.')
        return cleaned_data


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'register_number', 'department', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Full name'}),
            'register_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Register number'}),
            'department': forms.Select(attrs={'class': 'select-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'student@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '10 digit phone number'}),
        }


class IssueBookForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['student', 'book']
        widgets = {
            'student': forms.Select(attrs={'class': 'select-field'}),
            'book': forms.Select(attrs={'class': 'select-field'}),
        }

    def clean_book(self):
        book = self.cleaned_data.get('book')
        if book and book.available_quantity <= 0:
            raise forms.ValidationError(f'"{book.title}" is not currently available for issue.')
        return book


class ReturnBookForm(forms.Form):
    """Simple confirmation form used on the return-book page."""
    confirm = forms.BooleanField(
        required=True,
        label='Confirm this book has been physically returned',
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-field'})
    )
