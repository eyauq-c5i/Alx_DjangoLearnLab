from django.db import models

# 1. Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. Book Model (ForeignKey: One-to-Many)
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )

    def __str__(self):
        return self.title

# 3. Library Model (ManyToManyField: Many-to-Many)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# 4. Librarian Model (OneToOneField: One-to-One)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return f"{self.name} ({self.library.name})"