from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Existing Models ---

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.library.name})"

# --- New UserProfile Model for RBAC (Step 1) ---

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# --- Signals for Automatic UserProfile Creation ---

# This signal ensures a UserProfile is created immediately after a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile with the default role 'Member'
        UserProfile.objects.create(user=instance)

# This signal ensures the UserProfile is saved whenever the User is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This check prevents errors if the signal runs before the create signal on an existing user
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()