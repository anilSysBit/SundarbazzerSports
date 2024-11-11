from django import forms
from .models import Team,Payment,Player,Match
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


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




class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'team', 'name', 'jersey_no', 'age', 'email', 'phone', 'weight',
            'is_active', 'profile_image', 'height', 'blood_group', 'address',
            'designation'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'designation': forms.Select(),
            'blood_group': forms.Select(),
        }



"""

Match form 

"""


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['event', 'team1', 'team2', 'is_address_default', 'match_date', 'match_time', 'place', 'match_complete', 'notes']
        widgets = {
            'match_date': forms.DateInput(attrs={'type': 'date'}),
            'match_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        team1 = cleaned_data.get('team1')
        team2 = cleaned_data.get('team2')
        match_date = cleaned_data.get('match_date')
        match_time = cleaned_data.get('match_time')

        # 1. Check for same team combination (team1 and team2 must be unique)
        if team1 and team2 and team1 == team2:
            raise ValidationError("A team cannot play against itself.")
        

        # Check if there's an existing match between the same teams on the same date and time
        if team1 and team2 and match_date and match_time:
            existing_match = Match.objects.filter(
                match_date=match_date,
                match_time=match_time
            ).filter(
                (models.Q(team1=team1) & models.Q(team2=team2)) |
                (models.Q(team1=team2) & models.Q(team2=team1))
            ).exists()
            if existing_match:
                raise ValidationError("A match between these teams already exists at the same date and time.")

        # 2. Check if match_date is after event_start_date
        if event and match_date:

            print('Event Start date',event.event_start_date,match_date)
            if match_date < event.event_start_date:
                raise ValidationError({'match_date':f"Match date cannot be before the event start date ({event.event_start_date})."})


        