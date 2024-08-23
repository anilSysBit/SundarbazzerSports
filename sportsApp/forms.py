from django import forms
from .models import Team,Payment
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'total_players', 'sports_genere', 'email', 'address', 'logo', 'banner', 'gender']

    def save(self, commit=True):
        team = super().save(commit=False)
        if not team.pk and team.email:
            # Generate a random username
            username = team.email.split('@')[0] + get_random_string(5)
            
            # Create the user instance
            user = User.objects.create(
                username=username,
                email=team.email
            )
            
            # Set a random password
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            # Associate the user with the team
            team.user = user

            # Send email with credentials
            self._send_email(username, team.email, password)

        if commit:
            team.save()
        return team

    def _send_email(self, username, email, password):
        subject = 'Your Account Details'
        message = f"""
        Hi {username},

        Your account has been created successfully.

        Username: {username}
        Email: {email}
        Password: {password}

        Please keep these details safe.

        Regards,
        Your Team
        """
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)




