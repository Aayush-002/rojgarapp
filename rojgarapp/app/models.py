from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserDetails(models.Model):
    name = models.CharField(_("Name"), max_length=20)
    Email = models.EmailField(_("Email"))
    Gender = models.CharField(_("Gender"), max_length=7)
    PhoneNumber = models.CharField(_("Phone Number"), max_length=12)
    DOB = models.DateField(_("Date of Birth"))
    Skill = models.CharField(_("Skill"), max_length=25)
    Address = models.CharField(_("Address"), max_length=30)

    def __str__(self):
        return self.name
    

class AdminDetails(models.Model):
    name = models.CharField(_("Name"), max_length=20)
    Email = models.EmailField(_("Email"))
    Password = models.CharField(_("Password"), max_length=20)

    def __str__(self):
        return self.name

# Validators
def validate_file_size(file, max_size_mb):
    max_size_kb = max_size_mb * 1024  # Convert MB to KB
    if file.size > max_size_kb * 1024:
        raise ValidationError(
            _(f"File size should not exceed {max_size_mb} MB.")
        )

# Specific validators
def validate_photo_pp(file):
    validate_file_size(file, 1)  # 1 MB limit for Profile Photo

def validate_citizenship_photo(file):
    validate_file_size(file, 2)  # 2 MB limit for Citizenship Photos

def validate_cv_resume(file):
    validate_file_size(file, 5)  # 5 MB limit for Resume/CV



class PersonalDetails(models.Model):
    GENDER_CHOICES = [
        ("male", _("Male")),
        ("female", _("Female")),
        ("others", _("Others")),
    ]

    EDUCATION_CHOICES = [
        ("slc_see", _("SLC/SEE")),
        ("plus_two", _("+2")),
        ("bachelor", _("Bachelor")),
        ("masters", _("Masters")),
        ("diploma", _("Diploma")),
        ("uneducated", _("Uneducated")),
        ("class_eight_pass", _("Class 8 pass")),
        ("class_five_pass", _("Class 5 pass")),
    ]

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
    ]

    # Personal Information
    first_name = models.CharField(_("First Name"), max_length=100)
    middle_name = models.CharField(
        _("Middle Name"), max_length=100, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=100)
    dob = models.DateField(_("Date of Birth"))
    mobile_number = models.CharField(_("Mobile Number"), max_length=10)
    contact_number = models.CharField(
        _("Contact Number"), max_length=10, blank=True, null=True
    )
    email_address = models.EmailField(_("Email Address"), blank=True, null=True)
    national_id_number = models.CharField(
        _("National ID Number"), max_length=50, blank=True, null=True
    )
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER_CHOICES)
    citizenship_number = models.CharField(_("Citizenship Number"), max_length=50)
    citizenship_issued_date = models.DateField(_("Citizenship Issued Date"))
    citizenship_issued_district = models.CharField(
        _("Citizenship Issued District"), max_length=100
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    # Family Information
    fathers_name = models.CharField(_("Father's Name"), max_length=100)
    mothers_name = models.CharField(_("Mother's Name"), max_length=100)
    spouse_name = models.CharField(
        _("Spouse Name"), max_length=100, blank=True, null=True
    )

    # Address
    province = models.CharField(_("Province"), max_length=100)
    district = models.CharField(_("District"), max_length=100)
    municipality = models.CharField(_("Municipality"), max_length=100)
    ward_no = models.PositiveIntegerField(_("Ward No"))
    tole_name = models.CharField(_("Tole Name"), max_length=100)

    # Education and Professional Details
    education_background = models.CharField(
        _("Education Background"), max_length=20, choices=EDUCATION_CHOICES
    )
    professional_skill = models.TextField(_("Professional Skill"))

    # File Uploads
   # Profile Photo
    photo_pp = models.ImageField(
        _("Profile Photo"),
        upload_to="uploads/photos/",
        validators=[validate_photo_pp],  
    )
    # Citizenship Photo (Front)
    citizenship_photo_front = models.ImageField(
        _("Citizenship Photo (Front)"),
        upload_to="uploads/citizenship/",
        validators=[validate_citizenship_photo],  
    )
    # Citizenship Photo (Back)
    citizenship_photo_back = models.ImageField(
        _("Citizenship Photo (Back)"),
        upload_to="uploads/citizenship/",
        validators=[validate_citizenship_photo],  
    )
    # Resume/CV
    cv_resume = models.FileField(
        _("Resume/CV"),
        upload_to="uploads/resumes/",
        blank=True,
        null=True,
        validators=[validate_cv_resume],  
    )
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Professions(models.Model):
    name = models.CharField(_("Profession Name"), max_length=100)

    def __str__(self):
        return self.name
