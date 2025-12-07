from typing import Any

from django import forms
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from blog.models import Post, Comment, Tag
from blog.forms import UserRegisterForm, PostCreationForm, CommentForm, SearchForm, ProfileManagementForm

User = get_user_model
class RegisterView(CreateView):
    """Ä view to create new user instances"""

    template_name = 'register.html'
    form_class = UserRegisterForm
    model = User
    success_url = reverse_lazy('profile')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

class ProfileManagementView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    """A view to manage user profiles requires users to LogIn"""
    template_name = 'profile_management.html'
    model = User
    form_class = ProfileManagementForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileManagementForm(instance=user)
        context['user'] = self.request.user
        return context
    
    def get_success_url(self) -> str:
        return reverse ('profile')
    
    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:

        user_bio = form.cleaned_data.get('bio')
        user_photo = form.cleaned_data.get('profile_picture')
        user = self.request.user
        
        profile = user.profile  
        profile.bio = user_bio
        profile.profile_picture = user_photo
        profile.save()

        user.save()
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user == self.get_object()

class HomeView(TemplateView):
    template_name ='home.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    form_class = PostForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.has_perm('blog.add_post')
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def test_func(self):
        return self.is_owner()
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_create_post'] = self.request.user.has_perm('blog.add_post')
        return context

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context

    def post(self, request, *args, **kwargs):
        # Handles comment submission on the detail page
        if not request.user.is_authenticated:
            # redirect to login (you may want to preserve next param)
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.path)

        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect(self.request.path)  # refresh to show the new comment
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comment'] = self.get_object().post_comments.all()
        return context
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_pk = self.kwargs['post_pk']
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=post_pk)
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()  # make sure Post has get_absolute_url()


class CommentListView(ListView):
    """ A view to list all comments associated with a Post"""
    template_name = 'blog/comment_list.html'
    model = Comment
    context_object_name = 'comment_list'

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.post.get_absolute_url()
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.post.get_absolute_url()
class PostDetailCommentView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)




def search_view(request):
    queryset = Post.objects.all()
    form = SearchForm()

    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['to_search']
            searched_items = queryset.filter(Q(title__icontains=query)|Q(content__icontains=query))
        else:
            form = SearchForm()
    context = {
        'post_list': searched_items,
        'search_form': form,
    }
    return render(request, 'search.html', context=context)

def tag_view(request, tag_name):
    tag = get_object_or_404(klass=Tag, name__iexact=tag_name)
    post_by_tag = Post.objects.filter(Q(tags__name__icontains=tag.name))

    context = {
        'posts':post_by_tag,
        'tag_name':tag_name
    }

    return render(request, 'tags.html', context=context)

@login_required
@user_passes_test
def dummy(request):
    if request.method == "POST":
        form = RegisterForm(instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    return render(request, 'post_list.html', {'dummy':dummy})

def commentdummy(request, pk):
    return render(request, 'comment_create.html', {'dummy':dummy})

class PostByTagListView(ListView):
    model = Post
    template_name = 'tags.html'

tag_names = form.cleaned_data['tags'].split(',')
for t in tag_names:
    tag_obj, created = Tag.objects.get_or_create(name=t.strip())
    post.tags.add(tag_obj)

def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

def posts_by_tag(request, tag_name):
    posts = Post.objects.filter(tags__name__iexact=tag_name)
    return render(request, 'blog/posts_by_tag.html', {'posts': posts, 'tag_name': tag_name})
