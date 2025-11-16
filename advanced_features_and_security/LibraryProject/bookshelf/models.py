from django.db import models

# Create your models here.
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        # A helpful method for displaying the object in the shell/admin
        return f"{self.title} by {self.author}"
    
