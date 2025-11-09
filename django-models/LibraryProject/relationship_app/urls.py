from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# 1. Imports for existing application views
from .views import list_books, LibraryDetailView 

# 2. Module import for views.register, views.add_book, etc.
from . import views 

urlpatterns = [
    # --- Existing Application URL patterns ---
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns ---
    path('register/', views.register, name='register'), 
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # --- Role-Based Access URLs ---
    path('admin_area/', views.admin_view, name='admin_area'),
    path('librarian_desk/', views.librarian_view, name='librarian_desk'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),
    
    # --- Custom Permission Secured URLs ---
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
]