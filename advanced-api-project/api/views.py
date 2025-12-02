from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

# NEW imports for filtering / searching / ordering
from rest_framework.filters import SearchFilter, OrderingFilter
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

    # Step 1, 2, 3: Enable filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,  # filtering
        SearchFilter,         # searching
        OrderingFilter        # ordering
    ]

    # Filtering options (Step 1)
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching options (Step 2)
    search_fields = ['title', 'author']

    # Ordering options (Step 3)
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

    def get_queryset(self):
        """
        Add custom year filtering logic while keeping DRF filters active.
        """
        queryset = Book.objects.all()

        # Custom filter: ?year=YYYY
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(publication_year=year)

        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve one book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Custom behavior added in perform_create().
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom save logic
        print(f"Creating book from user: {self.request.user}")

        # Additional validation rule
        if serializer.validated_data["publication_year"] < 1500:
            raise ValidationError("Year must be 1500 or later.")

        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    Custom behavior added in perform_update().
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        print("A book is being updated!")
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Custom behavior added in perform_destroy().
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        print(f"Deleting book: {instance.title}")
        instance.delete()
