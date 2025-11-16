from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Article
from .models import Book  # Import your Book model
from .forms import SearchForm

# Unsafe (vulnerable to SQL injection)
# User.objects.raw(f"SELECT * FROM user WHERE username = '{username}'")

# Safe (uses ORM parameterization)
users = User.objects.filter(username=username)

@permission_required('yourapp.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, "articles/list.html", {"articles": articles})

@permission_required('yourapp.can_create', raise_exception=True)
def article_create(request):
    if request.method == "POST":
        # Create books...
        return redirect("article_list")
    return render(request, "articles/create.html")

@permission_required('yourapp.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        # Edit Book_list..
        return redirect("article_list")
    return render(request, "articles/edit.html", {"article": article})

@permission_required('yourapp.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect("article_list")
def book_list(request):
    books = Book.objects.all()  # Fetch all books
    context = {'books': books}
    return render(request, 'bookshelf/book_list.html', context)
# Create your views here.

def csp_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' ajax.googleapis.com"
        return response
    return middleware


def search_books(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.none()

    return render(request, 'bookshelf/search_results.html', {'books': books, 'form': form})
