from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import list_books, LibraryDetailView, register, admin_view, librarian_view, member_view, add_book, edit_book, delete_book

urlpatterns = [
    # --- Existing Application URL patterns ---
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns ---
    path('register/', register, name='register'), 
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # --- Role-Based Access URLs ---
    path('admin_area/', admin_view, name='admin_area'),
    path('librarian_desk/', librarian_view, name='librarian_desk'),
    path('member_dashboard/', member_view, name='member_dashboard'),
    
    # --- Custom Permission Secured URLs ---
    path('book/add/', add_book, name='add_book'),
    path('book/<int:pk>/edit/', edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', delete_book, name='delete_book'),
]