from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, register 

urlpatterns = [
    # 1. Function-Based View (list_books)
    path('', list_books, name='list_books'),
    
    # 2. Class-Based View (LibraryDetailView)
    # You need to include a primary key (pk) in the URL for DetailView
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns (Based on previous task's requirements) ---
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]