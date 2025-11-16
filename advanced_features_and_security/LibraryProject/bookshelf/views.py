from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Article

@permission_required('yourapp.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, "articles/list.html", {"articles": articles})

@permission_required('yourapp.can_create', raise_exception=True)
def article_create(request):
    if request.method == "POST":
        # Create logic here...
        return redirect("article_list")
    return render(request, "articles/create.html")

@permission_required('yourapp.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        # Edit logic here...
        return redirect("article_list")
    return render(request, "articles/edit.html", {"article": article})

@permission_required('yourapp.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect("article_list")

# Create your views here.
