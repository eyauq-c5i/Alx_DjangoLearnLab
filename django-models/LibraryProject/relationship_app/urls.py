from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # 1. URL for the Function-Based View (Lists all books)
    path('books/', views.book_list_view, name='book_list'),
    
    # 2. URL for the Class-Based View (Shows details for a specific library)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]