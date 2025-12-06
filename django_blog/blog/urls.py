from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login/logout
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),

    # Registration
    path("register/", views.register_view, name="register"),

    # Profile
    path("profile/", views.profile_view, name="profile"),
]
