from django.shortcuts import render

from rest_framework import generics, permissions, filters
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django_filters import rest_framework as filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    List all books.
    Includes filtering, searching, and ordering.
    Custom filtering by ?year=YYYY also preserved.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching
    search_fields = ['title', 'author']

    # Ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

    def get_queryset(self):
        queryset = Book.objects.all()

        # Custom filter ?year=YYYY
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(publication_year=year)

        return queryset


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Creating book from user: {self.request.user}")

        if serializer.validated_data["publication_year"] < 1500:
            raise ValidationError("Year must be 1500 or later.")

        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Supports:
    - /books/<pk>/update/
    - /books/update/?id=<pk>
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Support query parameter ID
        book_id = self.request.query_params.get("id")
        if book_id:
            return Book.objects.get(pk=book_id)

        return super().get_object()

    def perform_update(self, serializer):
        print("A book is being updated!")
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Supports:
    - /books/<pk>/delete/
    - /books/delete/?id=<pk>
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        book_id = self.request.query_params.get("id")
        if book_id:
            return Book.objects.get(pk=book_id)

        return super().get_object()

    def perform_destroy(self, instance):
        print(f"Deleting book: {instance.title}")
        instance.delete()
