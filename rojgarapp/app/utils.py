from django.db.models import Count
from .models import PersonalDetails

def get_gender_counts():
    genders = PersonalDetails.objects.values("gender").annotate(count=Count("id"))
    return {
        "male": next((entry["count"] for entry in genders if entry["gender"] == "male"), 0),
        "female": next((entry["count"] for entry in genders if entry["gender"] == "female"), 0),
        "others": next((entry["count"] for entry in genders if entry["gender"] == "others"), 0),
    }

def get_employment_status_counts():
    status_stats = PersonalDetails.objects.values("employment_status").annotate(count=Count("id"))
    return {
        "occupied": next((entry["count"] for entry in status_stats if entry["employment_status"] == "occupied"), 0),
        "unoccupied": next((entry["count"] for entry in status_stats if entry["employment_status"] == "unoccupied"), 0),
    }