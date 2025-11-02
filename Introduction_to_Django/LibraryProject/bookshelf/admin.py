from django.contrib import admin
from .models import Book # Import the Book model

# 1. Define the custom ModelAdmin class
class BookAdmin(admin.ModelAdmin):
    # Customize the list display columns:
    list_display = ('title', 'author', 'publication_year')

    # Add filters to the sidebar:
    list_filter = ('publication_year', 'author')

    # Add search capabilities (search by title and author):
    search_fields = ('title', 'author')

    # Add fields that are links to the change page:
    list_display_links = ('title',)

# 2. Register the model with the custom admin class
admin.site.register(Book, BookAdmin)