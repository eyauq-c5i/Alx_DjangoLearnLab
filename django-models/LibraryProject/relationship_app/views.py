from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView


# --- FUNCTION-BASED VIEW ---
def list_books(request):
    """
    Function-based view to display all books and their authors.
    """
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})


# --- CLASS-BASED VIEW ---
class LibraryDetailView(DetailView):
    """
    Class-based view to display details of a specific library,
    including all books in that library.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
