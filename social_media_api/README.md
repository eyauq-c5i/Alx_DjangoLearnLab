# Social Media API – Authentication Module

## Setup Instructions

1. Clone repository
2. Install dependencies:
   pip install django djangorestframework
3. Run migrations:
   python manage.py migrate
4. Start server:
   python manage.py runserver

## Authentication Flow

- Users register via `/api/accounts/register/`
- A token is returned upon successful registration
- Users login via `/api/accounts/login/`
- Token is used for authenticated requests

## User Model

Custom User extends AbstractUser and includes:
- bio
- profile_picture
- followers (ManyToMany self-reference)

## Authentication

Token-based authentication using Django REST Framework.

## Posts Endpoints

GET /api/posts/
POST /api/posts/
GET /api/posts/{id}/
PUT /api/posts/{id}/
DELETE /api/posts/{id}/

Supports pagination & search:
GET /api/posts/?search=keyword

## Comments Endpoints

GET /api/comments/
POST /api/comments/
GET /api/comments/{id}/
PUT /api/comments/{id}/
DELETE /api/comments/{id}/

## Authentication
All endpoints require Token Authentication

## Follow System

POST /api/accounts/follow/{user_id}/
POST /api/accounts/unfollow/{user_id}/

Users can follow and unfollow other users.
Self-following is not allowed.

## Feed Endpoint

GET /api/feed/

Returns posts created by users that the authenticated user follows.
Posts are ordered by most recent first.

Authentication required for all endpoints.

## Likes

POST /api/posts/{id}/like/
POST /api/posts/{id}/unlike/

Users can like a post only once.

## Notifications

GET /api/notifications/

Shows notifications for:
- New followers
- Likes on posts
- Comments on posts
