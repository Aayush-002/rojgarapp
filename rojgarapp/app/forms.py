from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import PersonalDetails, JobAnnouncement, CustomUser


def validate_phone_number(value):
    """Validate that phone number has exactly 10 digits after +977"""
    if not value.startswith('+977'):
        raise ValidationError('Phone number must start with +977')
    
    # Remove +977 and check if remaining part has exactly 10 digits
    number_part = value[4:]  # Remove '+977'
    if not number_part.isdigit() or len(number_part) != 10:
        raise ValidationError('Phone number must have exactly 10 digits after +977 (e.g., +9771234567890)')


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        help_text="Enter your phone number (e.g., +9771234567890)",
        widget=forms.TextInput(attrs={'class': 'form-control auth-input', 'placeholder': '+977'}),
        initial='+977',
        validators=[validate_phone_number]
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control auth-input'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control auth-input'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control auth-input'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control auth-input'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control auth-input'}),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Generate a unique username if not provided
        if not user.username:
            base_username = f"{user.first_name.lower()}{user.last_name.lower()}"
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
        return super().save(commit)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        # Validate format
        validate_phone_number(phone_number)
        
        # Check if already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already registered.")
        
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control auth-input', 'placeholder': '+977'}),
        label="Phone Number",
        initial='+977',
        validators=[validate_phone_number]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control auth-input'}),
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # Remove username field
        
        # Reorder fields to show phone_number first, then password
        field_order = ['phone_number', 'password']
        self.fields = {field: self.fields[field] for field in field_order}

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')

        if phone_number and password:
            self.user_cache = authenticate(
                self.request,
                phone_number=phone_number,
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid phone number or password."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = "__all__"

        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "photo_pp": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "citizenship_photo_front": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            ),
            "citizenship_photo_back": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            ),
            "cv_resume": forms.ClearableFileInput(attrs={"accept": ".pdf,.doc,.docx"}),
            "education_background": forms.Select(attrs={"class": "form-select"}),
        }

    status = forms.ChoiceField(
        choices=PersonalDetails.STATUS_CHOICES,
        required=False,
        initial="pending",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class JobAnnouncementForm(forms.ModelForm):
    class Meta:
        model = JobAnnouncement
        fields = ["title", "description", "required_personnel", "profession"]
