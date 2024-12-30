from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.auth_login, name="login"),
    path("register/", views.auth_signup, name="register"),
    path("logout/", views.auth_logout, name="logout"),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
