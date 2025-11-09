from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# 1. Explicit import for list_books and LibraryDetailView
from .views import list_books, LibraryDetailView 

# 2. Module import for views.register, views.admin_view, views.add_book, etc.
from . import views 

urlpatterns = [
    # --- Existing Application URL patterns (Using explicit imports) ---
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns ---
    path('register/', views.register, name='register'),
    
    # Must use LoginView.as_view(template_name=...
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Must use LogoutView.as_view(template_name=...
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # --- Role-Based Access URLs (Using views.dot notation) ---
    path('admin_area/', views.admin_view, name='admin_area'),
    path('librarian_desk/', views.librarian_view, name='librarian_desk'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),
    
    # --- Custom Permission Secured URLs (Using required paths) ---
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
]