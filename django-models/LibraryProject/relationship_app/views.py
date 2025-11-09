from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# --- 1. Function-Based View (FBV) ---
def book_list_view(request):
    """Lists all books in the database."""
    
    # Query all Book objects. Prefetching 'author' reduces database queries.
    books = Book.objects.all().select_related('author')
    
    context = {
        'books': books
    }
    # Renders the HTML template 'list_books.html'
    return render(request, 'list_books.html', context)

# --- 2. Class-Based View (CBV) ---
class LibraryDetailView(DetailView):
    """Displays details for a specific library."""
    
    # 1. Specify the model this view will operate on
    model = Library
    
    # 2. Specify the template to use for rendering
    template_name = 'library_detail.html'
    