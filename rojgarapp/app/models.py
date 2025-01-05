from django.db import models

# Create your models here.
class UserDetails(models.Model):
    name = models.CharField(max_length=20)
    Email = models.EmailField()
    Gender=models.CharField(max_length=7)
    PhoneNumber = models.CharField(max_length=12)
    DOB = models.DateField()
    Skill = models.CharField(max_length=25)
    Address = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    
class PersonalDetails(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ]

    EDUCATION_CHOICES = [
        ('slc_see', 'SLC/SEE'),
        ('plus_two', '+2'),
        ('bachelor', 'Bachelor'),
        ('masters', 'Masters'),
        ('diploma', 'Diploma'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    mobile_number = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=10, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    national_id_number = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    citizenship_number = models.CharField(max_length=50)
    citizenship_issued_date = models.DateField()
    citizenship_issued_district = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # Family Information
    fathers_name = models.CharField(max_length=100)
    mothers_name = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)

    # Address
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward_no = models.PositiveIntegerField()
    tole_name = models.CharField(max_length=100)

    # Education and Professional Details
    education_background = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    professional_skill = models.TextField()

    # File Uploads
    photo_pp = models.ImageField(upload_to='uploads/photos/')
    citizenship_photo_front = models.ImageField(upload_to='uploads/citizenship/')
    citizenship_photo_back = models.ImageField(upload_to='uploads/citizenship/')
    cv_resume = models.FileField(upload_to='uploads/resumes/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
