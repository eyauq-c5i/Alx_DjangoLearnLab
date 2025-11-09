import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings') 
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def setup_sample_data():
    """Creates sample data for demonstration."""
    print("--- Setting up Sample Data ---")

    # 1. Create Authors
    author_tolkien, created = Author.objects.get_or_create(name='J.R.R. Tolkien')
    author_rowling, created = Author.objects.get_or_create(name='J.K. Rowling')

    # 2. Create Books (ForeignKey relationship)
    book_hobbit, created = Book.objects.get_or_create(title='The Hobbit', author=author_tolkien)
    book_rings, created = Book.objects.get_or_create(title='The Lord of the Rings', author=author_tolkien)
    book_stone, created = Book.objects.get_or_create(title='Philosopher\'s Stone', author=author_rowling)

    # 3. Create Library
    library_central, created = Library.objects.get_or_create(name='City Central Library')
    
    # Add books to the Library (ManyToMany relationship)
    library_central.books.add(book_hobbit, book_rings)
    
    # 4. Create Librarian (OneToOne relationship)
    librarian_john, created = Librarian.objects.get_or_create(library=library_central, defaults={'name': 'John Smith'})
    
    print("Sample data loaded successfully.")


def run_queries():
    """Executes the required queries by fetching objects."""
    print("\n--- Running Queries ---")

    # --- Fetching necessary model instances ---
    # Fetch Author instance
    try:
        author_tolkien = Author.objects.get(name='J.R.R. Tolkien')
    except Author.DoesNotExist:
        print("Error: Author 'J.R.R. Tolkien' not found.")
        return

    # Fetch Library instance
    try:
        library_central = Library.objects.get(name='City Central Library')
    except Library.DoesNotExist:
        print("Error: Library 'City Central Library' not found.")
        return


    # Query 1: Query all books by a specific author (ForeignKey)
    print("1. Query all books by Author (J.R.R. Tolkien):")
    # Access the related books using the reverse manager 'books'
    tolkien_books = author_tolkien.books.all() 
    
    for book in tolkien_books:
        print(f"  - {book.title}")
    
    # Query 2: List all books in a library (ManyToManyField)
    print("\n2. List all books in a Library (City Central Library):")
    
    library_books = library_central.books.all()
    
    for book in library_books:
        print(f"  - {book.title}")

    # Query 3: Retrieve the librarian for a library (OneToOneField)
    print("\n3. Retrieve the Librarian for a Library:")
    
    try:
        # Use the reverse relationship name 'librarian'
        librarian = library_central.librarian
        print(f"  - Librarian: {librarian.name}")
    except Librarian.DoesNotExist:
        print("  - Error: Librarian not found.")


if __name__ == '__main__':
    # Clean up data to prevent integrity errors on rerun
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Run setup and queries
    setup_sample_data()
    run_queries()