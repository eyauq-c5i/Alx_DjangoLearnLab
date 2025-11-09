from django.urls import path
from .views import list_books, LibraryDetailView, register, login_user, logout_user

urlpatterns = [
    path('', list_books, name='list_books'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
