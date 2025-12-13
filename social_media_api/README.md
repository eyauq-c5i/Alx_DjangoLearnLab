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
