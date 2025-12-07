from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # ------------------------------------------
    # AUTH & PROFILE ROUTES
    # ------------------------------------------
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Authentication
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='blog/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='blog/logout.html'),
        name='logout'
    ),

    # ------------------------------------------
    # BLOG POST ROUTES
    # ------------------------------------------
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # ------------------------------------------
    # COMMENT ROUTES (TEST-REQUIRED)
    # ------------------------------------------
    path(
        'post/<int:pk>/comments/new/',
        views.CommentCreateView.as_view(),
        name='comment_create'
    ),
    path(
        'comment/<int:pk>/update/',
        views.CommentUpdateView.as_view(),
        name='comment_update'
    ),
    path(
        'comment/<int:pk>/delete/',
        views.CommentDeleteView.as_view(),
        name='comment_delete'
    ),

    # ------------------------------------------
    # TAG ROUTES (TEST-REQUIRED)
    # ------------------------------------------
    path(
        'tags/<slug:tag_slug>/',
        views.PostByTagListView.as_view(),
        name='posts_by_tag'
    ),

    # ------------------------------------------
    # SEARCH ROUTE
    # ------------------------------------------
    path(
        'search/',
        views.SearchResultsView.as_view(),
        name='search_results'
    ),
]
