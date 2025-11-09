from django.urls import path
from .views import list_books, register, login_user, logout_user
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', list_books, name='list_books'),  # existing view
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
