from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=15,
        unique=True,
        help_text=_("Enter your phone number (e.g., +9771234567890)"),
    )

    email = models.EmailField(blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserDetails(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=20)
    Email = models.EmailField(verbose_name=_("Email"))
    Gender = models.CharField(verbose_name=_("Gender"), max_length=7)
    PhoneNumber = models.CharField(verbose_name=_("Phone Number"), max_length=12)
    DOB = models.DateField(verbose_name=_("Date of Birth"))
    Skill = models.CharField(verbose_name=_("Skill"), max_length=25)
    Address = models.CharField(verbose_name=_("Address"), max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("User Detail")
        verbose_name_plural = _("User Details")


# Validators
def validate_file_size(file, max_size_mb):
    max_size_kb = max_size_mb * 1024  # Convert MB to KB
    if file.size > max_size_kb * 1024:
        raise ValidationError(_(f"File size should not exceed {max_size_mb} MB."))


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
        ("phd", _("PHD")),
        ("uneducated", _("Uneducated")),
        ("class_eight_pass", _("Class 8 pass")),
        ("class_five_pass", _("Class 5 pass")),
    ]

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
    ]

    PROFESSION_CHOICES = [
        ("teacher", _("Teacher")),
        ("doctor", _("Doctor")),
        ("engineer", _("Engineer")),
        ("labor", _("Labor")),
        ("driver", _("Driver")),
        ("jyami", _("Jyami")),
        ("mistri", _("Mistri")),
        ("electrician", _("Electrician")),
        ("plumber", _("Plumber")),
        ("painter", _("Painter")),
        ("mason", _("Mason")),
        ("mechanic", _("Mechanic")),
        ("welder", _("Welder")),
        ("carpenter", _("Carpenter")),
        ("tailor", _("Tailor")),
        ("agricultural_worker", _("Agricultural Worker")),
        ("construction_worker", _("Construction Worker")),
        ("porter", _("Porter")),
        ("cleaner", _("Cleaner")),
        ("waiter", _("Waiter")),
        ("cook", _("Cook")),
        ("security_guard", _("Security Guard")),
        ("delivery_person", _("Delivery Person")),
        ("shop_assistant", _("Shop Assistant")),
        ("street_vendor", _("Street Vendor")),
        ("butcher", _("Butcher")),
        ("fisherman", _("Fisherman")),
        ("rickshaw_driver", _("Rickshaw Driver")),
        ("barber", _("Barber")),
        ("fruit_seller", _("Fruit Seller")),
        ("taxi_driver", _("Taxi Driver")),
        ("auto_rickshaw_driver", _("Auto Rickshaw Driver")),
        ("garbage_collector", _("Garbage Collector")),
        ("other", _("Other")),
    ]

    # Personal Information
    first_name = models.CharField(verbose_name=_("First Name"), max_length=100)
    middle_name = models.CharField(
        verbose_name=_("Middle Name"), max_length=100, blank=True, null=True
    )
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=100)
    dob = models.DateField(verbose_name=_("Date of Birth"))
    mobile_number = models.CharField(verbose_name=_("Mobile Number"), max_length=10)
    contact_number = models.CharField(
        verbose_name=_("Contact Number"), max_length=10, blank=True, null=True
    )
    email_address = models.EmailField(
        verbose_name=_("Email Address"), blank=True, null=True
    )
    national_id_number = models.CharField(
        verbose_name=_("National ID Number"), max_length=50, blank=True, null=True
    )
    gender = models.CharField(
        verbose_name=_("Gender"), max_length=10, choices=GENDER_CHOICES
    )
    citizenship_number = models.CharField(
        verbose_name=_("Citizenship Number"), max_length=50
    )
    citizenship_issued_date = models.DateField(
        verbose_name=_("Citizenship Issued Date")
    )
    citizenship_issued_district = models.CharField(
        verbose_name=_("Citizenship Issued District"), max_length=100
    )
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)

    # Family Information
    fathers_name = models.CharField(verbose_name=_("Father's Name"), max_length=100)
    mothers_name = models.CharField(verbose_name=_("Mother's Name"), max_length=100)
    spouse_name = models.CharField(
        verbose_name=_("Spouse Name"), max_length=100, blank=True, null=True
    )

    # Address
    province = models.CharField(verbose_name=_("Province"), max_length=100)
    district = models.CharField(verbose_name=_("District"), max_length=100)
    municipality = models.CharField(verbose_name=_("Municipality"), max_length=100)
    ward_no = models.PositiveIntegerField(verbose_name=_("Ward No"))
    tole_name = models.CharField(verbose_name=_("Tole Name"), max_length=100)

    # Education and Professional Details
    education_background = models.CharField(
        verbose_name=_("Education Background"), max_length=20, choices=EDUCATION_CHOICES
    )
    professional_skill = models.CharField(
        verbose_name=_("Professional Skill"), 
        max_length=50, 
        choices=PROFESSION_CHOICES
    )

    # File Uploads
    # Profile Photo
    photo_pp = models.ImageField(
        verbose_name=_("Profile Photo"),
        upload_to="uploads/photos/",
        validators=[validate_photo_pp],
    )
    # Citizenship Photo (Front)
    citizenship_photo_front = models.ImageField(
        verbose_name=_("Citizenship Photo (Front)"),
        upload_to="uploads/citizenship/",
        validators=[validate_citizenship_photo],
    )
    # Citizenship Photo (Back)
    citizenship_photo_back = models.ImageField(
        verbose_name=_("Citizenship Photo (Back)"),
        upload_to="uploads/citizenship/",
        validators=[validate_citizenship_photo],
    )
    # Resume/CV
    cv_resume = models.FileField(
        verbose_name=_("Resume/CV"),
        upload_to="uploads/resumes/",
        blank=True,
        null=True,
        validators=[validate_cv_resume],
    )
    # Status
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        null=True,
        blank=True,
    )
    employment_status = models.CharField(
        verbose_name=_("Employment Status"),
        max_length=20,
        choices=[("occupied", _("Occupied")), ("unoccupied", _("Unoccupied"))],
        default="unoccupied",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Personal Detail")
        verbose_name_plural = _("Personal Details")


class Professions(models.Model):
    name = models.CharField(verbose_name=_("Profession Name"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Profession")
        verbose_name_plural = _("Professions")


class JobAnnouncement(models.Model):
    title = models.CharField(verbose_name=_("Job Title"), max_length=200)
    description = models.TextField(verbose_name=_("Job Description"))
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Posted By")
    )
    posted_date = models.DateTimeField(verbose_name=_("Posted Date"), auto_now_add=True)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    required_personnel = models.PositiveIntegerField(
        verbose_name=_("Required Personnel"), default=1
    )
    profession = models.CharField(
        verbose_name=_("Profession"),
        max_length=50,
        choices=PersonalDetails.PROFESSION_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Job Announcement")
        verbose_name_plural = _("Job Announcements")


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("reviewed", _("Reviewed")),
        ("accepted", _("Accepted")),
        ("rejected", _("Rejected")),
    ]

    job = models.ForeignKey(
        JobAnnouncement,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name=_("Job"),
    )
    applicant = models.ForeignKey(
        PersonalDetails,
        on_delete=models.CASCADE,
        related_name="job_applications",
        verbose_name=_("Applicant"),
    )
    application_date = models.DateTimeField(_("Application Date"), auto_now_add=True)
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    class Meta:
        verbose_name = _("Job Application")
        verbose_name_plural = _("Job Applications")
        unique_together = ("job", "applicant")
        ordering = ["-application_date"]

    def __str__(self):
        return f"{self.applicant} - {self.job}"

    def clean(self):
        # Only check limit when trying to accept an application
        if self.status == "accepted":
            # Count current accepted applications (excluding this one if it's being updated)
            current_accepted = self.job.applications.filter(status="accepted")
            if self.pk:
                current_accepted = current_accepted.exclude(pk=self.pk)

            if current_accepted.count() >= self.job.required_personnel:
                raise ValidationError(
                    _("This job has already reached the maximum number of applicants.")
                )

    def save(self, *args, **kwargs):
        old_status = None
        if self.pk:
            old_status = JobApplication.objects.get(pk=self.pk).status

        self.full_clean()
        super().save(*args, **kwargs)

        # Check if status changed to 'accepted'
        if self.status == "accepted" and old_status != "accepted":
            self.applicant.employment_status = "occupied"
            self.applicant.save()

        elif old_status == "accepted" and self.status != "accepted":
            self.applicant.employment_status = "unoccupied"
            self.applicant.save()
