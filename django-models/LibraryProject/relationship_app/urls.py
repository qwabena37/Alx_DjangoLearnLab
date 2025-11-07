from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # import your views module

urlpatterns = [
    # Register view (function-based)
    path('register/', views.register_view, name='register'),

    # Login view (class-based view from Django, with custom template)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout view (class-based view from Django, with custom template)
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Existing views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
