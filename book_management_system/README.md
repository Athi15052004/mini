# College Library - Book Management System (Pure CSS / Vanilla JS Edition)

A complete, production-quality **Book Management System** for a college library, built with
**Django (Python)**, **SQLite3**, and **plain HTML5 / CSS3 / Vanilla JavaScript** —
no Bootstrap, Tailwind, jQuery, React, Angular, Vue, or any other front-end framework,
and no CDN dependencies. Everything runs fully offline, which makes it suitable for
older Windows 7 lab computers with outdated or no internet access.

Suitable as an M.Sc. Computer Science mini project.

---

## Why no frameworks / no CDN?

- All CSS is hand-written in `static/css/style.css` using **Flexbox** and basic layout
  techniques that work in older browsers.
- All JavaScript is hand-written in `static/js/script.js` using plain ES5-style syntax
  (no arrow functions relied upon for critical logic, no `let`/`const`-only patterns that
  would break in very old engines, no external libraries).
- No `<script src="https://...">` or `<link href="https://...">` tags anywhere — every
  asset is served locally by Django's staticfiles app, so the system works with **zero
  internet connection**.
- Confirmation dialogs (e.g. "Delete this book?") are implemented as a simple CSS
  overlay + vanilla JS `openModal()` / `closeModal()` functions instead of a Bootstrap modal.

---

## Features

- **Admin Authentication** — login, logout, session management, password validation (Django's built-in auth system)
- **Dashboard** — total books, available books, issued books, returned books, total students, recent activity feed
- **Book Management** — add / view / update / delete, search, filter by category and author
- **Student Management** — add / view / edit / delete students
- **Borrow & Return Module** — issue book, return book, issue/return dates, availability checks, prevents issuing unavailable books
- **Search** — by title, author, ISBN, or category
- **Custom, framework-free UI** — fixed sidebar, top bar, dashboard cards, responsive tables, pagination, CSS hover effects, mobile-friendly layout
- **Custom 404 / 500 error pages**
- **CSRF protection, form validation, messages framework, delete confirmations**

---

## Project Structure

```
BookManagementSystem/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                  (created after migration)
├── BookManagementSystem/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│   └── asgi.py
├── library/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── books.html
│   ├── add_book.html
│   ├── edit_book.html
│   ├── students.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── issue_book.html
│   ├── return_book.html
│   ├── profile.html
│   ├── 404.html
│   ├── 500.html
│   └── includes/pagination.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
└── media/
```

---

## Setup Instructions

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create an admin (superuser) account

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Open the application

Visit **http://127.0.0.1:8000/** and log in with the superuser credentials created above.
The Django admin panel is available at **http://127.0.0.1:8000/admin/**.

Because there are no external CDN links, the site will render and function correctly
even with the lab computer fully disconnected from the internet (as long as the Django
development server itself is reachable, e.g. on localhost).

---

## Running Tests

```bash
python manage.py test
```

Covers Book/Student model behaviour, the full issue → return workflow (availability
increments/decrements correctly), blocking issue of unavailable books, and login
enforcement.

---

## Notes for Reviewers / Evaluators

- All views that touch data require login (`@login_required`); unauthenticated users
  are redirected to the login page.
- The `Borrow` model tracks `issue_date`, `return_date`, and `status` (Issued/Returned).
  Issuing a book decrements `Book.available_quantity`; returning increments it back.
  The system refuses to issue a book with zero `available_quantity` — this is checked
  both in the form (`IssueBookForm.clean_book`) and again in the view for safety.
- Search across books uses Django ORM `Q` objects to match title, author, ISBN, or
  category in a single query; students can be searched by name, register number,
  email, or department.
- Pagination uses Django's built-in `Paginator` (10 rows per page).
- Delete confirmation is a pure CSS/JS modal overlay — see `openModal()` /
  `closeModal()` in `static/js/script.js`.
- The `SECRET_KEY` and `DEBUG=True` in `settings.py` are suitable for local
  development / academic demonstration only.

---

## License

This project was created for academic / educational purposes.
