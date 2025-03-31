from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from .forms import PersonalDetailsForm, JobAnnouncementForm
from .models import PersonalDetails, Professions, JobAnnouncement
from django.utils.translation import gettext_lazy as _
from django.db.models import Count


@login_required
def home(request):
    current_year = datetime.now().year
    notices = JobAnnouncement.objects.filter(is_active=True).order_by("-posted_date")
    return render(
        request, "app/index.html", {"current_year": current_year, "notices": notices}
    )


@login_required
def dashboard(request):
    user_count = PersonalDetails.objects.count()
    registered_users = (
        PersonalDetails.objects.values("ward_no")
        .annotate(count=Count("id"))
        .order_by("ward_no")
    )
    genders = PersonalDetails.objects.values("gender").annotate(count=Count("id"))
    male_count = next(
        (entry["count"] for entry in genders if entry["gender"] == "male"), 0
    )
    female_count = next(
        (entry["count"] for entry in genders if entry["gender"] == "female"), 0
    )
    others_count = next(
        (entry["count"] for entry in genders if entry["gender"] == "others"), 0
    )

    # Add employment status counts
    status_stats = PersonalDetails.objects.values("employment_status").annotate(
        count=Count("id")
    )
    occupied_count = next(
        (
            entry["count"]
            for entry in status_stats
            if entry["employment_status"] == "occupied"
        ),
        0,
    )
    unoccupied_count = next(
        (
            entry["count"]
            for entry in status_stats
            if entry["employment_status"] == "unoccupied"
        ),
        0,
    )

    ward_numbers = [entry["ward_no"] for entry in registered_users]
    ward_counts = [entry["count"] for entry in registered_users]

    professions_count = (
        PersonalDetails.objects.values("professional_skill")
        .annotate(count=Count("id"))
        .order_by("professional_skill")
    )
    list_professions_count = list(professions_count)

    return render(
        request,
        "app/dashboard.html",
        {
            "ward_numbers": ward_numbers,
            "ward_counts": ward_counts,
            "user_count": user_count,
            "male_count": male_count,
            "female_count": female_count,
            "others_count": others_count,
            "professions_count": list_professions_count,
            "occupied_count": occupied_count,
            "unoccupied_count": unoccupied_count,
        },
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

        # Validate the form
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

        # Create the user
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


# create forms
def forms(request):
    editForm = False
    professions = Professions.objects.all()
    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            print("validation pass is here!")
            form.save()
            messages.success(request, "Successfully registered")
            return redirect("forms_list", {"professions": professions})
        else:
            print("Validation failed!")
            print(f"Form errors: {form.errors}")  # status error
            messages.error(request, "त्रुटि भयो, कृपया त्रुटिहरू सच्याउनुहोस् र अगेन भर्नुहोस्.")
    else:
        form = PersonalDetailsForm()

    return render(
        request,
        "app/forms.html",
        {"form": form, "editForm": editForm, "professions": professions},
    )


# show list of submitted forms
@login_required
def forms_list(request):
    forms = PersonalDetails.objects.order_by("-created_at")
    if request.method == "GET":
        list = request.GET.get("form_search")
        if list != None:
            forms = PersonalDetails.objects.filter(first_name__icontains=list)
            print("forms", forms)

    return render(request, "app/forms_list.html", {"forms": forms})


# edit_forms
@login_required
def forms_edit(request, form_id):
    edit_form = get_object_or_404(PersonalDetails, pk=form_id)
    editForm = True
    professions = Professions.objects.all()
    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES, instance=edit_form)

        status_value = request.POST.get("status", "pending").lower()

        form.data = form.data.copy()
        form.data["status"] = status_value

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated")
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
            "editForm": editForm,
            "professions": professions,
        },
    )


# delete form
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
