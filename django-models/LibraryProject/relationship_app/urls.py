from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, register_view as register

urlpatterns = [
    # Existing URL pattern
    path('', list_books, name='list_books'),
    # path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication URL Patterns ---

    # 1. Registration: Uses the aliased function 'register'
    path('register/', register, name='register'),
    
    # 2. Login: Uses the built-in Class-Based View (CBV) as required
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # 3. Logout: Uses the built-in Class-Based View (CBV) as required
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]