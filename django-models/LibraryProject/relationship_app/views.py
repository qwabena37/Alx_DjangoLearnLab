from django.shortcuts import render
from django.views.generic.detail import DetailView  # Explicit import for DetailView
from .models import Book, Library
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm



# -------------------------
# Function-Based View
# -------------------------
def list_books(request):
    """Displays a list of all books and their authors."""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# -------------------------
# Class-Based View
# -------------------------
class LibraryDetailView(DetailView):
    """Displays details of a specific library and its books."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# relationship_app/views.py

# -----------------------------
# REGISTER VIEW
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('list_books')  # redirect to a page after registration
    else:
        form = RegisterForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# -----------------------------
# LOGIN VIEW
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('list_books')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# -----------------------------
# LOGOUT VIEW
# -----------------------------
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # <-- instantiate with POST data
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('list_books')
    else:
        form = UserCreationForm()  # <-- instantiate empty form for GET request

    return render(request, 'relationship_app/register.html', {'form': form})
