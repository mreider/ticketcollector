from .models import Profile

def save_profile(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        profile.avatar = url
    profile.save()
