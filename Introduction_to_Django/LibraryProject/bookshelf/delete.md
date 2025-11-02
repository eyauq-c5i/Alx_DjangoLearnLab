# Delete Operation

Command:
```python
from bookshelf.models import Book
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four") # Assuming the book was successfully updated in the prior step
book_to_delete.delete()
print(Book.objects.all())