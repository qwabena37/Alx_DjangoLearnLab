from django.urls import path
from . import views
from .views import follow_user, unfollow_user, UserListView, RegisterView, LoginView, profile


urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
]
