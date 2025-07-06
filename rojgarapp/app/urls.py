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
    path('applications/', views.applications_list, name='application_list'),
    path('applications/update-status/', views.update_application_status, name='update_application_status'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path("post-job/", views.post_job, name="post_job"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),
    path("job/<int:job_id>/apply/", views.apply_job, name="apply_job"),
]
