from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.auth_login, name="login"),
    path("register/", views.auth_signup, name="register"),
    path("forms/", views.user_details_view, name="forms"),
    path("logout/", views.auth_logout, name="logout"),
]
