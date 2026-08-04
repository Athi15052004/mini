from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Book, Student, Borrow


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Django for Beginners',
            author='William Vincent',
            isbn='9781234567890',
            category='Computer Science',
            publisher='WSV Books',
            publication_year=2022,
            quantity=5,
            available_quantity=5,
        )

    def test_book_str(self):
        self.assertIn('Django for Beginners', str(self.book))

    def test_is_available(self):
        self.assertTrue(self.book.is_available())
        self.book.available_quantity = 0
        self.book.save()
        self.assertFalse(self.book.is_available())


class StudentModelTest(TestCase):
    def test_create_student(self):
        student = Student.objects.create(
            name='John Doe',
            register_number='REG2024001',
            department='MSc CS',
            email='john@example.com',
            phone='9876543210',
        )
        self.assertEqual(str(student), 'John Doe (REG2024001)')


class BorrowFlowTest(TestCase):
    """Verifies that issuing a book decreases availability and returning it restores availability."""

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='testpass123')
        self.client = Client()
        self.client.login(username='admin', password='testpass123')

        self.book = Book.objects.create(
            title='Clean Code',
            author='Robert C. Martin',
            isbn='9780132350884',
            category='Computer Science',
            publisher='Prentice Hall',
            publication_year=2008,
            quantity=2,
            available_quantity=2,
        )
        self.student = Student.objects.create(
            name='Jane Smith',
            register_number='REG2024002',
            department='MSc CS',
            email='jane@example.com',
            phone='9876543211',
        )

    def test_issue_book_decreases_availability(self):
        self.client.post(reverse('issue_book'), {
            'student': self.student.pk,
            'book': self.book.pk,
        })
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_quantity, 1)
        self.assertEqual(Borrow.objects.filter(status='Issued').count(), 1)

    def test_cannot_issue_unavailable_book(self):
        self.book.available_quantity = 0
        self.book.save()
        self.client.post(reverse('issue_book'), {
            'student': self.student.pk,
            'book': self.book.pk,
        })
        self.assertEqual(Borrow.objects.filter(status='Issued').count(), 0)

    def test_return_book_increases_availability(self):
        borrow = Borrow.objects.create(student=self.student, book=self.book, status='Issued')
        self.book.available_quantity -= 1
        self.book.save()

        self.client.post(reverse('return_book', args=[borrow.pk]), {'confirm': True})
        self.book.refresh_from_db()
        borrow.refresh_from_db()

        self.assertEqual(borrow.status, 'Returned')
        self.assertEqual(self.book.available_quantity, 2)


class AuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='testpass123')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # redirected to login

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
