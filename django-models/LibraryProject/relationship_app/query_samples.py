# Setup necessary to run standalone script in a Django environment
import os
import django

# NOTE: Replace 'django-models' with the name of your main project folder if it is different
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
    # The primary_key=True in the Librarian model means we must use create or get_or_create
    # with the library instance passed.
    librarian_john, created = Librarian.objects.get_or_create(library=library_central, defaults={'name': 'John Smith'})
    
    print("Sample data loaded successfully.")
    return author_tolkien, library_central

def run_queries(author_tolkien, library_central):
    """Executes the required queries."""
    print("\n--- Running Queries ---")

    # Query 1: Query all books by a specific author (ForeignKey)
    print("1. Query all books by Author (J.R.R. Tolkien):")
    tolkien_books = author_tolkien.books.all() 
    
    for book in tolkien_books:
        print(f"  - {book.title}")
    
    # Query 2: List all books in a library (ManyToManyField)
    print("\n2. List all books in a Library (City Central Library):")
    
    # Uses the default ManyToMany manager name: 'books'
    library_books = library_central.books.all()
    
    for book in library_books:
        print(f"  - {book.title}")

    # Query 3: Retrieve the librarian for a library (OneToOneField)
    print("\n3. Retrieve the Librarian for a Library:")
    
    # Uses the default OneToOne reverse manager name: 'librarian'
    try:
        librarian = library_central.librarian
        print(f"  - Librarian: {librarian.name}")
    except Librarian.DoesNotExist:
        print("  - Error: Librarian not found.")


if __name__ == '__main__':
    # Clean up data to prevent integrity errors on rerun
    Book.objects.all().delete()
    Author.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Run setup and queries
    author, library = setup_sample_data()
    run_queries(author, library)