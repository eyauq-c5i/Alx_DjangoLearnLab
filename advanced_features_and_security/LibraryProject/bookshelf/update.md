# Update Operation

Command:
```python
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
print(Book.objects.get(author="George Orwell").title)