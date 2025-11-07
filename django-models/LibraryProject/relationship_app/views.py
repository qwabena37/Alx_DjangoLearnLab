from django.shortcuts import render
from django.views.generic.detail import DetailView  # <-- Added import
from .models import Book, Library


# -------------------------
# Function-Based View
# -------------------------
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# -------------------------
# Class-Based View
# -------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
