from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Book
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create books
        self.book1 = Book.objects.create(
            title="Alpha",
            author="Author A",
            publication_year=2000
        )
        self.book2 = Book.objects.create(
            title="Beta",
            author="Author B",
            publication_year=2010
        )

        self.client = APIClient()

    # ----------------
    # LIST VIEW TESTS
    # ----------------
    def test_list_books(self):
        """Ensure the list endpoint returns all books."""
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_year(self):
        """Test custom filtering: ?year=2000"""
        url = reverse("book-list")
        response = self.client.get(url, {"year": 2000})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["publication_year"], 2000)

    def test_search_books(self):
        """Test search functionality."""
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Alpha"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Alpha")

    def test_order_books(self):
        """Test ordering: ?ordering=title"""
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-title"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Beta")  # B comes after A

    # ----------------
    # DETAIL VIEW TEST
    # ----------------
    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Alpha")

    # ----------------
    # CREATE TESTS
    # ----------------
    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books."""
        url = reverse("book-create")
        data = {
            "title": "New Book",
            "author": "Someone",
            "publication_year": 2020,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Authenticated users can create."""
        self.client.login(username="testuser", password="password123")

        url = reverse("book-create")
        data = {
            "title": "New Book",
            "author": "Someone",
            "publication_year": 2020,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ----------------
    # UPDATE TESTS
    # ----------------
    def test_update_book_authenticated(self):
        """Authenticated users can update books."""
        self.client.login(username="testuser", password="password123")

        url = reverse("book-update", args=[self.book1.id])
        data = {
            "title": "Updated Title",
            "author": "Author A",
            "publication_year": 2000,
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        """Unauthenticated users cannot update."""
        url = reverse("book-update", args=[self.book1.id])
        data = {
            "title": "Blocked Update",
            "author": "Author A",
            "publication_year": 2000,
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------
    # DELETE TESTS
    # ----------------
    def test_delete_book_authenticated(self):
        """Authenticated user can delete."""
        self.client.login(username="testuser", password="password123")

        url = reverse("book-delete", args=[self.book2.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Unauthenticated user should fail."""
        url = reverse("book-delete", args=[self.book1.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
