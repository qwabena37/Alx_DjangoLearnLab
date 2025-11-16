from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Article
from .models import Book  # Import your Book model

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
