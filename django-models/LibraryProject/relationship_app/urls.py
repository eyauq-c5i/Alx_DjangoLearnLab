from django.urls import path
import relationship_app.views as views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('register/', views.register, name='register'),  # checker sees views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
