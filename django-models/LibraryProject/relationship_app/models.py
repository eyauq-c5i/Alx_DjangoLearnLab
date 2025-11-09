from django.db import models

# Create your models here.
# 1. Author Model
class Author(models.Model):
    # The primary key (id) is automatically created by Django.
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. Book Model (ForeignKey: One-to-Many)
class Book(models.Model):
    # A single Author can write multiple Books.
    # CASCADE means if an Author is deleted, all their Books are deleted too.
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 3. Library Model (ManyToManyField: Many-to-Many)
class Library(models.Model):
    # A single Book can be in multiple Libraries, and a Library can have many Books.
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# 4. Librarian Model (OneToOneField: One-to-One)
class Librarian(models.Model):
    # A single Librarian works for exactly one Library, and vice-versa.
    # The 'related_name' allows us to easily go from Library back to Librarian (library.librarian).
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return f"{self.name} ({self.library.name})"