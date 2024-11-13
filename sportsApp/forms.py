from django import forms
from .models import Team,Payment,Player,Match,EventTeam,Event
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from address.models import Province,District,Municipality,Area
today = date.today()



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
    def __init__(self, *args, **kwargs):
            # Capture the selected event if passed as an argument
            event = kwargs.pop('event', None)
            super().__init__(*args, **kwargs)
            
            # If an event is specified, filter teams to those related to that event
            if event:
                self.fields['team1'].queryset = EventTeam.objects.filter(event=event)
                self.fields['team2'].queryset = EventTeam.objects.filter(event=event)
            else:
                # Default to an empty queryset if no event is provided
                self.fields['team1'].queryset = EventTeam.objects.none()
                self.fields['team2'].queryset = EventTeam.objects.none()


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
     
        # Check if both event and match_date are provided
        if event and match_date:
            print('Event Start date:', event.event_start_date, 'Match date:', match_date)
                      # Compare match_date with event_start_date
            if match_date < today:
                raise ValidationError({'match_date': f"Invalid Date Selected , Select the time ahead of now"})
                retu
            event_start_date_only = event.event_start_date.date()
             # Compare match_date with event_start_date
            if match_date < event_start_date_only:
                raise ValidationError({'match_date': f"Match date cannot be before the event start date ({event_start_date_only})."})
            
  
            # Compare today's date with event_start_date



""" Event form"""
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'event_type', 'status', 'banner', 'logo', 'event_organizer', 
            'event_age_limit', 'is_verified', 'entry_fee', 'registration_start_date', 
            'registration_end_date', 'event_start_date', 'event_end_date', 
            'match_duration','province','district','municipality','area',
        ]
        widgets = {
            'registration_start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'match_duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label="Select Province")
    district = forms.ModelChoiceField(queryset=District.objects.none(), empty_label="Select District")
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none(), empty_label="Select Municipality")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prepopulate dependent fields if it's an edit (if the form instance already exists)
        if self.instance and self.instance.pk:
            # Prepopulate the district, municipality, and area based on the current Event instance
            self.fields['district'].queryset = District.objects.filter(province=self.instance.province)
            self.fields['municipality'].queryset = Municipality.objects.filter(district=self.instance.district)

            # Set initial values to ensure they are selected in the form (during update)
            self.initial['district'] = self.instance.district
            self.initial['municipality'] = self.instance.municipality

        # Dynamically update queryset based on previously selected values during form submission
        if 'province' in self.data:
            province_id = self.data.get('province')
            if province_id:
                self.fields['district'].queryset = District.objects.filter(province_id=province_id)
            else:
                self.fields['district'].queryset = District.objects.none()

        if 'district' in self.data:
            district_id = self.data.get('district')
            if district_id:
                self.fields['municipality'].queryset = Municipality.objects.filter(district_id=district_id)
            else:
                self.fields['municipality'].queryset = Municipality.objects.none()

    # Optional: You can add custom validation if needed
    def clean_entry_fee(self):
        fee = self.cleaned_data.get('entry_fee')
        if fee < 0:
            raise forms.ValidationError(_('Entry fee must be positive.'))
        return fee