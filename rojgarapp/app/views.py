from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from datetime import datetime
from .forms import PersonalDetailsForm, JobAnnouncementForm
from .models import PersonalDetails, Professions, JobAnnouncement, JobApplication
from .utils import get_gender_counts, get_employment_status_counts, get_status_badge_class

def check_employer(user):
    return user.groups.filter(name="Employers").exists()

@login_required
def home(request):
    jobs = JobAnnouncement.objects.filter(is_active=True).order_by("-posted_date")
    return render(
        request, "app/index.html", {"jobs": jobs}
    )


@login_required
def dashboard(request):
    user_count = PersonalDetails.objects.count()
    registered_users = (
        PersonalDetails.objects.values("ward_no")
        .annotate(count=Count("id"))
        .order_by("ward_no")
    )
    ward_numbers = [entry["ward_no"] for entry in registered_users]
    ward_counts = [entry["count"] for entry in registered_users]

    professions_count = (
        PersonalDetails.objects.values("professional_skill")
        .annotate(count=Count("id"))
        .order_by("professional_skill")
    )

    gender_counts = get_gender_counts()
    employment_status_counts = get_employment_status_counts()

    context = {
        "ward_numbers": ward_numbers,
        "ward_counts": ward_counts,
        "user_count": user_count,
        "male_count": gender_counts["male"],
        "female_count": gender_counts["female"],
        "others_count": gender_counts["others"],
        "professions_count": list(professions_count),
        "occupied_count": employment_status_counts["occupied"],
        "unoccupied_count": employment_status_counts["unoccupied"],
    }

    return render(
        request,
        "app/dashboard.html",
        context,
    )


def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")


def auth_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login")
    return render(request, "auth/signup.html")


def auth_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("login")


def forms(request):
    editForm = False
    professions = Professions.objects.all()
    is_employer = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Employers").exists()
    )

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered!")
            return redirect("forms_list")
        else:
            messages.error(request, "Something went wrong, please try again later.")
    else:
        form = PersonalDetailsForm()

    return render(
        request,
        "app/forms.html",
        {
            "form": form,
            "editForm": editForm,
            "professions": professions,
            "is_employer": is_employer,
        },
    )


@login_required
def forms_list(request):
    forms = PersonalDetails.objects.order_by("-created_at")
    if request.method == "GET":
        search_query = request.GET.get("form_search")
        if search_query:
            forms = PersonalDetails.objects.filter(first_name__icontains=search_query)

    return render(request, "app/forms_list.html", {"forms": forms})


@login_required
def forms_edit(request, form_id):
    edit_form = get_object_or_404(PersonalDetails, pk=form_id)
    professions = Professions.objects.all()
    is_employer = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Employers").exists()
    )

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES, instance=edit_form)
        form.data = form.data.copy()
        form.data["status"] = request.POST.get("status", "pending").lower()

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated!")
            return redirect("forms_list")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = PersonalDetailsForm(instance=edit_form)

    return render(
        request,
        "app/forms.html",
        {
            "form": form,
            "editForm": True,
            "professions": professions,
            "is_employer": is_employer,
        },
    )


@login_required
def forms_delete(request, form_id):
    delete_form = get_object_or_404(PersonalDetails, pk=form_id)
    if request.method == "POST":
        delete_form.delete()
        messages.success(request, "Successfully deleted")
        return redirect("forms_list")
    return render(
        request, "app/forms_confirm_delete.html", {"delete_form": delete_form}
    )


@login_required
def post_job(request):
    if not request.user.groups.filter(name="Employers").exists():
        messages.error(request, "Only employers can post jobs.")
        return redirect("home")

    if request.method == "POST":
        form = JobAnnouncementForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("home")
        else:
            messages.error(request, "Error posting job. Please correct the form.")
    else:
        form = JobAnnouncementForm()

    return render(request, "app/post_job.html", {"form": form})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobAnnouncement, pk=job_id, is_active=True)
    applications = job.applications.all()
    has_applied = False
    user_application = None

    if request.user.is_authenticated:
        try:
            personal_details = PersonalDetails.objects.get(pk=request.user.id)
            has_applied = applications.filter(applicant=personal_details).exists()
            if has_applied:
                user_application = applications.get(applicant=personal_details)
        except PersonalDetails.DoesNotExist:
            pass

    accepted_count = applications.filter(status='accepted').count()
    
    context = {
        "job": job,
        "applications": applications,
        "accepted_count": accepted_count,
        "has_applied": has_applied,
        "user_application": user_application,
    }
    return render(request, "app/job_detail.html", context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobAnnouncement, pk=job_id, is_active=True)
    
    try:
        personal_details = PersonalDetails.objects.get(pk=request.user.id)
    except PersonalDetails.DoesNotExist:
        messages.error(request, "You need to fill out your personal details first.")
        return redirect("forms")

    if job.applications.filter(applicant=personal_details).exists():
        messages.error(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job.id)

    # Check if job has available positions
    accepted_applications = job.applications.filter(status='accepted').count()
    if accepted_applications >= job.required_personnel:
        messages.warning(request, "This job has already reached the maximum number of applicants.")
        return redirect('job_detail', job_id=job.id)

    JobApplication.objects.create(
        job=job,
        applicant=personal_details,
        status='pending'
    )
    
    messages.success(request, "Application submitted successfully!")
    return redirect('job_detail', job_id=job.id)

@login_required
def applications_list(request):
    if check_employer(request.user):
        applications = JobApplication.objects.filter(job__posted_by=request.user)
    else:
        applications = JobApplication.objects.filter(applicant__id=request.user.id)

    paginator = Paginator(applications, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    is_employer = check_employer(request.user)

    context = {
        "applications": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "is_employer": is_employer,
        "status_choices": JobApplication.STATUS_CHOICES,
    }

    return render(request, "app/applications_list.html", context)

@login_required
def update_application_status(request):
    if request.method == "POST" and check_employer(request.user):
        application_id = request.POST.get("application_id")
        new_status = request.POST.get("status")

        try:
            application = JobApplication.objects.get(pk=application_id, job__posted_by=request.user)
            application.status = new_status
            application.save()
            return JsonResponse({
                'success': True,
                'new_status': application.get_status_display(),
                'status_class': get_status_badge_class(new_status)
            })
        except JobApplication.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Application not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    
    # Check if user is the job poster
    if application.job.posted_by != request.user:
        messages.error(request, "You are not authorized to delete this application.")
        return redirect('applications_list')

    if request.method == "POST":
        application.delete()
        messages.success(request, "Application deleted successfully!")
        return redirect('applications_list')

    context = { "application": application }

    return render(request, "app/application_confirm_delete.html", context)