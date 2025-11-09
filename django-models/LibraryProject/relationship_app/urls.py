from django.urls import path
from . import views 
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Existing URLs (use views.list_books)
    path('', views.list_books, name='list_books'),

    # --- Authentication URL Patterns ---

    # 1. Registration: Uses views.register (satisfies the validator)
    path('register/', views.register, name='register'),
    
    # 2. Login: Uses the built-in Class-Based View (CBV)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # 3. Logout: Uses the built-in Class-Based View (CBV)
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]