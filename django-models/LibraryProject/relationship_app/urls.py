from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView
from . import views

urlpatterns = [
    # Existing URL patterns
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-based access
    path('admin_area/', views.admin_view, name='admin_area'),
    path('librarian_desk/', views.librarian_view, name='librarian_desk'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),

    # --- Custom Permission Secured URLs (Updated) ---
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]
