from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from .forms import PersonalDetailsForm
from .models import UserDetails


@login_required
def home(request):
    current_year = datetime.now().year
    return render(request, "app/index.html", {"current_year": current_year})


@login_required
def dashboard(request):
    return render(request, "app/dashboard.html")


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


# def forms(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         Email = request.POST.get('Email')
#         Gender = request.POST.get('Gender')
#         PhoneNumber = request.POST.get('PhoneNumber')
#         DOB = request.POST.get('DOB')
#         Skill = request.POST.get('Skill')
#         Address = request.POST.get('Address')

#         query  = UserDetails(name = name,Email = Email,Gender = Gender, 
#                              PhoneNumber = PhoneNumber,DOB = DOB,
#                              Skill = Skill, Address = Address)
#         query.save()
#         messages.success(request,"Successfully registered")
#         return redirect('/forms')
        

#     return render(request, "app/forms.html")

def forms(request):
    if request.method =="POST":
        form = PersonalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully registered")
            return redirect('home')
        else:
            messages.error(request, "त्रुटि भयो, कृपया त्रुटिहरू सच्याउनुहोस् र अगेन भर्नुहोस्.")
    else:
        form = PersonalDetailsForm()
    print(form)
    return render(request,"app/forms.html",{'form':form})






    # if request.method == 'POST':
    #     form = UserDetailsForm(request.POST, request.FILES)  # Include `request.FILES` for file uploads
    #     if form.is_valid():
    #         print(form.cleaned_data)
            
    #         # Redirect to a success page
    #         return HttpResponseRedirect('/success/')
    # else:
    #     form = UserDetailsForm()

    # return render(request, 'app/forms.html', {'form': form})