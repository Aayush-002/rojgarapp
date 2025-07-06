from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError

from .forms import PersonalDetailsForm, JobAnnouncementForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import PersonalDetails, JobAnnouncement, JobApplication
from .utils import (
    get_gender_counts,
    get_employment_status_counts,
    get_status_badge_class,
    check_employer,
    get_user_profile_status,
)


@login_required
def home(request):
    jobs = JobAnnouncement.objects.filter(is_active=True).order_by("-posted_date")
    
    # Get user profile status
    profile_status = get_user_profile_status(request.user)
    
    context = {
        "jobs": jobs,
        "profile_status": profile_status,
    }
    
    return render(request, "app/index.html", context)


@login_required
def dashboard(request):
    user_count = PersonalDetails.objects.count()

    # Get job statistics
    total_jobs = JobAnnouncement.objects.count()
    filled_jobs = (
        JobAnnouncement.objects.filter(applications__status="accepted")
        .distinct()
        .count()
    )
    active_jobs = JobAnnouncement.objects.filter(is_active=True).count()

    # Get profession counts with percentage
    professions_count = list(
        PersonalDetails.objects.values("professional_skill")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Calculate percentages for professions and get display names
    for profession in professions_count:
        profession["percentage"] = (
            round((profession["count"] / user_count * 100), 1) if user_count > 0 else 0
        )
        # Get display name from choices
        profession["display_name"] = dict(PersonalDetails.PROFESSION_CHOICES).get(
            profession["professional_skill"], profession["professional_skill"]
        )

    # Get job statistics by profession
    jobs_by_profession = (
        JobAnnouncement.objects.exclude(profession__isnull=True)
        .values("profession")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Prepare data for jobs by profession chart
    profession_names = []
    profession_counts = []
    for job in jobs_by_profession:
        profession_code = job["profession"]
        profession_name = dict(PersonalDetails.PROFESSION_CHOICES).get(profession_code, profession_code)
        profession_names.append(profession_name)
        profession_counts.append(job["count"])

    # If no jobs with professions, provide default empty lists
    if not profession_names:
        profession_names = []
        profession_counts = []

    # Get application status statistics
    application_stats = (
        JobApplication.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    # Prepare data for application status chart
    status_labels = [app["status"] for app in application_stats]
    status_counts = [app["count"] for app in application_stats]

    # Get monthly job posting trends (last 6 months)
    from django.db.models.functions import TruncMonth
    from datetime import datetime, timedelta

    six_months_ago = datetime.now() - timedelta(days=180)

    monthly_jobs = (
        JobAnnouncement.objects.filter(posted_date__gte=six_months_ago)
        .annotate(month=TruncMonth("posted_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    job_months = [entry["month"].strftime("%B %Y") for entry in monthly_jobs]
    job_counts = [entry["count"] for entry in monthly_jobs]

    # Get ward-wise statistics
    registered_users = (
        PersonalDetails.objects.values("ward_no")
        .annotate(count=Count("id"))
        .order_by("ward_no")
    )
    ward_numbers = [entry["ward_no"] for entry in registered_users]
    ward_counts = [entry["count"] for entry in registered_users]

    gender_counts = get_gender_counts()
    employment_status_counts = get_employment_status_counts()

    # Calculate application success rate
    total_applications = JobApplication.objects.count()
    successful_applications = JobApplication.objects.filter(status="accepted").count()
    application_success_rate = (
        (successful_applications / total_applications * 100)
        if total_applications > 0
        else 0
    )

    context = {
        "ward_numbers": ward_numbers,
        "ward_counts": ward_counts,
        "user_count": user_count,
        "total_jobs": total_jobs,
        "filled_jobs": filled_jobs,
        "active_jobs": active_jobs,
        "male_count": gender_counts["male"],
        "female_count": gender_counts["female"],
        "others_count": gender_counts["others"],
        "proffessions_count": professions_count,
        "profession_names": profession_names,
        "profession_counts": profession_counts,
        "status_labels": status_labels,
        "status_counts": status_counts,
        "job_months": job_months,
        "job_counts": job_counts,
        "application_success_rate": round(application_success_rate, 1),
        "occupied_count": employment_status_counts["occupied"],
        "unoccupied_count": employment_status_counts["unoccupied"],
    }

    return render(request, "app/dashboard.html", context)


def auth_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("home")
        else:
            messages.error(request, "Invalid phone number or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "auth/login.html", {"form": form})


def auth_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, "Account created successfully!")
                return redirect("login")
            except IntegrityError as e:
                if "username" in str(e):
                    messages.error(request, "Username already exists. Please choose a different username.")
                elif "phone_number" in str(e):
                    messages.error(request, "Phone number already registered. Please use a different phone number.")
                elif "email" in str(e):
                    messages.error(request, "Email already registered. Please use a different email address.")
                else:
                    messages.error(request, "Registration failed. Please try again with different information.")
            except Exception as e:
                messages.error(request, "An error occurred during registration. Please try again.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, "auth/signup.html", {"form": form})


def auth_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("login")


@login_required
def forms(request):
    editForm = False
    professions = PersonalDetails.PROFESSION_CHOICES
    is_employer = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Employers").exists()
    )

    # Get user profile status
    profile_status = get_user_profile_status(request.user)
    
    # If user already has personal details, redirect to edit
    if profile_status['has_profile']:
        return redirect('forms_edit', form_id=request.user.id)

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            personal_details = form.save(commit=False)
            personal_details.id = request.user.id  # Link to user
            personal_details.save()
            messages.success(request, "Personal details registered successfully!")
            return redirect("forms_list")
        else:
            messages.error(request, "Please correct the errors below.")
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
            "profile_status": profile_status,
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
    # Ensure user can only edit their own profile
    if request.user.id != form_id:
        messages.error(request, "You can only edit your own profile.")
        return redirect("forms")
    
    edit_form = get_object_or_404(PersonalDetails, pk=form_id)
    professions = PersonalDetails.PROFESSION_CHOICES
    is_employer = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Employers").exists()
    )
    
    # Get user profile status
    profile_status = get_user_profile_status(request.user)

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES, instance=edit_form)
        form.data = form.data.copy()
        form.data["status"] = request.POST.get("status", "pending").lower()

        if form.is_valid():
            form.save()
            messages.success(request, "Personal details updated successfully!")
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
            "profile_status": profile_status,
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

    # Get user profile status
    profile_status = get_user_profile_status(request.user)

    if request.user.is_authenticated:
        try:
            personal_details = PersonalDetails.objects.get(pk=request.user.id)
            has_applied = applications.filter(applicant=personal_details).exists()
            if has_applied:
                user_application = applications.get(applicant=personal_details)
        except PersonalDetails.DoesNotExist:
            pass

    accepted_count = applications.filter(status="accepted").count()

    context = {
        "job": job,
        "applications": applications,
        "accepted_count": accepted_count,
        "has_applied": has_applied,
        "user_application": user_application,
        "profile_status": profile_status,
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
        return redirect("job_detail", job_id=job.id)

    # Check if job has available positions
    accepted_applications = job.applications.filter(status="accepted").count()
    if accepted_applications >= job.required_personnel:
        messages.warning(
            request, "This job has already reached the maximum number of applicants."
        )
        return redirect("job_detail", job_id=job.id)

    JobApplication.objects.create(job=job, applicant=personal_details, status="pending")

    messages.success(request, "Application submitted successfully!")
    return redirect("job_detail", job_id=job.id)


@login_required
def applications_list(request):
    if check_employer(request.user):
        applications = JobApplication.objects.filter(job__posted_by=request.user)
    else:
        try:
            personal_details = PersonalDetails.objects.get(pk=request.user.id)
            applications = JobApplication.objects.filter(applicant=personal_details)
        except PersonalDetails.DoesNotExist:
            applications = JobApplication.objects.none()

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
            application = JobApplication.objects.get(
                pk=application_id, job__posted_by=request.user
            )
            application.status = new_status
            application.save()
            return JsonResponse(
                {
                    "success": True,
                    "new_status": application.get_status_display(),
                    "status_class": get_status_badge_class(new_status),
                }
            )
        except JobApplication.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Application not found"}, status=404
            )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    # Check if user is the job poster
    if application.job.posted_by != request.user:
        messages.error(request, "You are not authorized to delete this application.")
        return redirect("applications_list")

    if request.method == "POST":
        application.delete()
        messages.success(request, "Application deleted successfully!")
        return redirect("applications_list")

    context = {"application": application}

    return render(request, "app/application_confirm_delete.html", context)
