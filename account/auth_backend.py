from django.contrib.auth.backends import ModelBackend
from .models import Profile


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""

    def authenticate(self, email=None):
        
        if email is not None:
            try:
                return Profile.objects.get(email=email)
            except Profile.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(
                pk=user_id
            )
        except Profile.DoesNotExist:
            return None
