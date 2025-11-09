from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
# New Imports for RBAC
from .models import UserProfile 
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# --- Existing Application Views ---

# Function-Based View
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- User Authentication View (Renamed to 'register' for validator) ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # The signal automatically creates the UserProfile with role 'Member'
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Role Check Functions ---

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# --- Role-Based Views (Step 2) ---

@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    """View accessible only to Admin users."""
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """View accessible only to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """View accessible only to Member users."""
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})