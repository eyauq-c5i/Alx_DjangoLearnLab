from django.db import models


class Author(models.Model):
    """
    Represents a book author.
    Each author can have multiple books (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an author.
    Each book is linked to one Author using a ForeignKey.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',     # Allows reverse lookup: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
