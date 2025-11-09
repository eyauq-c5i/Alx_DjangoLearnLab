from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, register 


urlpatterns = [
    path('', list_books, name='list_books'),

    # Authentication URL Patterns matching the validator's expectation:
    path('register/', register, name='register'),
    
    # Use Django's built-in Class-Based Views (CBVs)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]