import os
import sys
import django
import random
from datetime import datetime, timedelta

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(project_dir))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rojgarapp.settings")
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User, Group
from app.models import PersonalDetails, Professions, JobAnnouncement, JobApplication


def create_groups():
    """Create necessary groups"""
    employers_group, _ = Group.objects.get_or_create(name="Employers")
    return employers_group


def create_users():
    """Create test users"""
    # Create employer users
    employers = []
    for i in range(1, 6):
        username = f"employer{i}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "first_name": f"Employer{i}",
                "last_name": "Test",
            },
        )
        if created:
            user.set_password("password123")
            user.save()
            employers_group = Group.objects.get(name="Employers")
            employers_group.user_set.add(user)
        employers.append(user)

    # Create regular users
    regular_users = []
    for i in range(1, 21):
        username = f"user{i}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "first_name": f"User{i}",
                "last_name": "Test",
            },
        )
        if created:
            user.set_password("password123")
            user.save()
        regular_users.append(user)

    return employers, regular_users


def create_professions():
    """Create test professions"""
    professions_list = [
        "Doctor",
        "Nurse",
        "Teacher",
        "Engineer",
        "Plumber",
        "Electrician",
        "Carpenter",
        "Chef",
        "Driver",
        "Security Guard",
        "Cleaner",
        "Gardener",
        "Painter",
        "Mason",
        "Mechanic",
    ]

    professions = []
    for prof_name in professions_list:
        profession, _ = Professions.objects.get_or_create(name=prof_name)
        professions.append(profession)

    return professions


def create_personal_details(users, professions):
    """Create personal details for users"""
    genders = ["male", "female", "others"]
    employment_statuses = ["employed", "unemployed"]
    districts = ["Kathmandu", "Lalitpur", "Bhaktapur"]
    provinces = ["Bagmati"]
    education_backgrounds = ["SLC", "Plus Two", "Bachelor", "Master"]

    for user in users:
        # Skip if personal details already exist
        if PersonalDetails.objects.filter(email_address=user.email).exists():
            continue

        # Generate random citizenship number
        citizenship_number = f"{random.randint(1000, 9999)}-{random.randint(100, 999)}"

        PersonalDetails.objects.create(
            first_name=user.first_name,
            middle_name="",
            last_name=user.last_name,
            gender=random.choice(genders),
            dob=datetime.now()
            - timedelta(days=random.randint(6570, 18250)),  # 18-50 years
            mobile_number=f"98{random.randint(10000000, 99999999)}",
            contact_number=f"01{random.randint(1000000, 9999999)}",
            email_address=user.email,
            province=random.choice(provinces),
            district=random.choice(districts),
            municipality=f"{random.choice(districts)} Metropolitan City",
            ward_no=random.randint(1, 32),
            tole_name=f"Tole {random.randint(1, 10)}",
            fathers_name=f"Father {random.randint(1, 100)}",
            mothers_name=f"Mother {random.randint(1, 100)}",
            spouse_name=(
                f"Spouse {random.randint(1, 100)}"
                if random.choice([True, False])
                else ""
            ),
            citizenship_number=citizenship_number,
            citizenship_issued_district=random.choice(districts),
            citizenship_issued_date=datetime.now()
            - timedelta(days=random.randint(365, 3650)),
            education_background=random.choice(education_backgrounds),
            professional_skill=random.choice(professions).name,
            employment_status=random.choice(employment_statuses),
            status="pending",
        )


def create_job_announcements(employers, professions):
    """Create test job announcements"""
    job_titles = [
        "Senior {}",
        "Junior {}",
        "Experienced {}",
        "Entry Level {}",
        "{} Needed",
        "Urgent Need for {}",
    ]

    for _ in range(30):  # Create 30 job announcements
        profession = random.choice(professions)
        title = random.choice(job_titles).format(profession.name)

        # Create job with random date within last 6 months
        posted_date = datetime.now() - timedelta(days=random.randint(0, 180))

        JobAnnouncement.objects.create(
            title=title,
            description=f"We are looking for a skilled {profession.name} to join our team.",
            profession=profession,
            required_personnel=random.randint(1, 5),
            posted_by=random.choice(employers),
            posted_date=posted_date,
            is_active=random.choice(
                [True, True, True, False]
            ),  # 75% chance of being active
        )


def create_job_applications(users, jobs):
    """Create test job applications"""
    statuses = ["pending", "accepted", "rejected"]

    for job in jobs:
        # Check if job has reached maximum applicants
        accepted_count = job.applications.filter(status="accepted").count()
        if accepted_count >= job.required_personnel:
            continue

        # Calculate how many more applications we can accept
        remaining_slots = job.required_personnel - accepted_count

        # Get random number of applications for this job
        # Make sure we don't exceed remaining slots
        max_new_applications = min(
            5, remaining_slots * 2
        )  # Allow 2x applications per slot
        num_applications = random.randint(0, max_new_applications)

        # Get all existing applicants for this job
        existing_applicants = set(
            job.applications.all().values_list("applicant__email_address", flat=True)
        )

        # Get available users (those who haven't applied)
        available_users = [
            user for user in users if user.email not in existing_applicants
        ]

        if not available_users or num_applications == 0:
            continue

        selected_users = random.sample(
            available_users, min(num_applications, len(available_users))
        )

        for user in selected_users:
            try:
                applicant = PersonalDetails.objects.get(email_address=user.email)
                # For new applications, bias towards pending status
                status_weights = [
                    ("pending", 0.7),
                    ("accepted", 0.2 if accepted_count < job.required_personnel else 0),
                    ("rejected", 0.1),
                ]

                # Calculate actual status based on weights
                status = random.choices(
                    [s[0] for s in status_weights],
                    weights=[s[1] for s in status_weights],
                )[0]

                # Only create accepted application if we haven't reached the limit
                if status == "accepted" and accepted_count >= job.required_personnel:
                    status = "pending"

                JobApplication.objects.create(
                    job=job, applicant=applicant, status=status
                )

                # Update accepted count if we just created an accepted application
                if status == "accepted":
                    accepted_count += 1

            except PersonalDetails.DoesNotExist:
                continue


def main():
    print("Creating groups...")
    employers_group = create_groups()

    print("Creating users...")
    employers, regular_users = create_users()

    print("Creating professions...")
    professions = create_professions()

    print("Creating personal details...")
    create_personal_details(regular_users, professions)

    print("Creating job announcements...")
    create_job_announcements(employers, professions)

    print("Creating job applications...")
    jobs = JobAnnouncement.objects.all()
    create_job_applications(regular_users, jobs)

    print("Data population completed!")


if __name__ == "__main__":
    main()
