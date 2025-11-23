from django.db import models

class Book(models.Model):
    """
    Book model representing a simple record of books.

    Fields:
        - title: Title of the book (string, max length 100)
        - author: Author of the book (string, max length 100)
    """

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return f"{self.title} by {self.author}"

