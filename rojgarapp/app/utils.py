from django.contrib.auth.models import Group
from .models import PersonalDetails
from django.db.models import Count

def check_employer(user):
    """Check if user is an employer"""
    return user.groups.filter(name="Employers").exists()

def get_user_profile_status(user):
    """
    Get user's profile completion status
    Returns: dict with profile_status, completion_percentage, personal_details
    """
    try:
        personal_details = PersonalDetails.objects.get(pk=user.id)
        is_complete = personal_details.is_profile_complete()
        completion_percentage = personal_details.get_profile_completion_percentage()
        
        return {
            'profile_status': 'complete' if is_complete else 'incomplete',
            'completion_percentage': completion_percentage,
            'personal_details': personal_details,
            'has_profile': True
        }
    except PersonalDetails.DoesNotExist:
        return {
            'profile_status': 'missing',
            'completion_percentage': 0,
            'personal_details': None,
            'has_profile': False
        }

def get_gender_counts():
    """Get gender distribution counts"""
    genders = PersonalDetails.objects.values("gender").annotate(count=Count("id"))
    counts = {'male': 0, 'female': 0, 'others': 0}
    
    for item in genders:
        counts[item['gender']] = item['count']
    
    return counts

def get_employment_status_counts():
    """Get employment status distribution counts"""
    status_stats = PersonalDetails.objects.values("employment_status").annotate(count=Count("id"))
    counts = {'occupied': 0, 'unoccupied': 0}
    
    for item in status_stats:
        counts[item['employment_status']] = item['count']
    
    return counts

def get_status_badge_class(status: str):
    if status == 'accepted':
        return 'bg-success'
    elif status == 'rejected':
        return 'bg-danger'
    elif status == 'pending':
        return 'bg-warning'
    return 'bg-info'