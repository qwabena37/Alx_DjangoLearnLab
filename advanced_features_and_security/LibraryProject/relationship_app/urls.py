from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # import your views module
from .views import list_books

urlpatterns = [
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    # Register view (function-based)
    path('register/', views.register_view, name='register'),

    # Login view (class-based view from Django, with custom template)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout view (class-based view from Django, with custom template)
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Existing views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # URL for adding a book
    path('add_book/', views.add_book, name='add_book'),
    
    # URL for editing a book by its primary key (id)
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    
    # You can also include delete_book if needed
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]
