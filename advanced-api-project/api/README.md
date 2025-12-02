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
