from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import list_books, LibraryDetailView 

from . import views

urlpatterns = [
    # Existing URL patterns
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns ---
    
    # Registration: Use views.register to satisfy the specific validator requirement
    path('register/', views.register, name='register'),
    
    # Login: Use the built-in Class-Based View (CBV) as required
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Logout: Use the built-in Class-Based View (CBV) as required
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]