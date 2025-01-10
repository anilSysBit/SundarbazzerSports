from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import re

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the provided username is an email address
            if re.match(r"[^@]+@[^@]+\.[^@]+", username):  # Simple email validation regex
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)

            # Check password
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None