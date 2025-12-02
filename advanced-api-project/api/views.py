from django.shortcuts import render


from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    List all books.
    Custom behavior added in get_queryset() for filtering.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Step 3: Custom behavior (filter by year using ?year=YYYY)
        queryset = Book.objects.all()
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
        # Step 3: Custom save logic
        print(f"Creating book from user: {self.request.user}")

        # Example: Additional validation rule
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

