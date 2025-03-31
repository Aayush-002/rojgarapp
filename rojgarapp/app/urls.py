from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.auth_login, name="login"),
    path("register/", views.auth_signup, name="register"),
    path("logout/", views.auth_logout, name="logout"),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forms/", views.forms, name="forms"),
    path("forms_list/", views.forms_list, name="forms_list"),
    path("<int:form_id>/edit/", views.forms_edit, name="forms_edit"),
    path("<int:form_id>/delete/", views.forms_delete, name="forms_delete"),
    path("post-job/", views.post_job, name="post_job"),
]
