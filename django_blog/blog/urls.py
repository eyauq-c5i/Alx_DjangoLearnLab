from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # AUTH & PROFILE ROUTES
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Login & logout
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # BLOG POST CRUD ROUTES

    # List + Detail
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    # Create
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),

    # Update (FIXED)
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),

    # Delete
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
