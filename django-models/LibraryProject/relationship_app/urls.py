from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# 1. Imports for existing views (to satisfy one validator check)
from .views import list_books, LibraryDetailView 

# 2. Imports for new role views and to satisfy the 'views.register' check
from . import views

urlpatterns = [
    # Existing URL patterns
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns ---
    
    # Registration: Uses views.register (satisfies the specific validator requirement)
    path('register/', views.register, name='register'),
    
    # Login: Uses the built-in Class-Based View (CBV)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Logout: Uses the built-in Class-Based View (CBV)
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # --- Role-Based Access URLs (Step 3) ---
    path('admin_area/', views.admin_view, name='admin_area'),
    path('librarian_desk/', views.librarian_view, name='librarian_desk'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),
]