# API Views Overview

This project uses Django REST Framework's generic class-based views to manage
CRUD operations for the Book model.

## Endpoints

- GET /api/books/ — List all books
- GET /api/books/<id>/ — Retrieve a book
- POST /api/books/create/ — Create a book (authenticated only)
- PUT /api/books/<id>/update/ — Update a book (authenticated only)
- DELETE /api/books/<id>/delete/ — Delete a book (authenticated only)

## Permissions
Unauthenticated users:
- Can read (ListView, DetailView)

Authenticated users:
- Can create, update, and delete books


sql
Filtering, Searching, and Ordering
----------------------------------

The BookListView API supports advanced query features:

Filtering:
- Filter by title, author, or publication_year.
  Example: /api/books/?author=Rowling

Search:
- Full-text search on title and author.
  Example: /api/books/?search=harry

Ordering:
- Order results by 'title' or 'publication_year'.
  Example: /api/books/?ordering=-publication_year
