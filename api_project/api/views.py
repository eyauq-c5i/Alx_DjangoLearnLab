from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    Read-only view that lists all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Public access for listing books


class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for the Book model.

    Provides:
    - list (GET /books_all/)
    - retrieve (GET /books_all/<id>/)
    - create (POST /books_all/)
    - update (PUT /books_all/<id>/)
    - partial_update (PATCH /books_all/<id>/)
    - destroy (DELETE /books_all/<id>/)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Auth required for write, read allowed for all


def home(request):
    """
    Root endpoint for the Book API.

    Provides a simple JSON response guiding users to available endpoints.
    """
    return JsonResponse({
        "message": "Welcome to the Book API",
        "endpoints": {
            "list_books": "/api/books/",
            "crud_books": "/api/books_all/"
        }
    })
