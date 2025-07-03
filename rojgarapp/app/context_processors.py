from .utils import get_user_profile_status


def profile_status(request):
    """
    Context processor to make profile status available in all templates
    """
    if request.user.is_authenticated:
        return {'profile_status': get_user_profile_status(request.user)}
    return {'profile_status': None} 