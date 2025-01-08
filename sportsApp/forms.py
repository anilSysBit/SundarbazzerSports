from django import forms
from .models import Team,Payment,Player,EventTeam,Event
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from address.models import Province,District,Municipality,Area
from django.utils import timezone
today = date.today()

class AddressMixin(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label="Select Province")
    district = forms.ModelChoiceField(queryset=District.objects.none(), empty_label="Select District")
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none(), empty_label="Select Municipality")
    # area = forms.ModelChoiceField(queryset=Area.objects.none(), empty_label="Select Area")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prepopulate fields if instance exists and has values
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'province') and self.instance.province:
                self.fields['district'].queryset = District.objects.filter(province=self.instance.province)
            if hasattr(self.instance, 'district') and self.instance.district:
                self.fields['municipality'].queryset = Municipality.objects.filter(district=self.instance.district)
            # if hasattr(self.instance, 'municipality') and self.instance.municipality:
            #     self.fields['area'].queryset = Area.objects.filter(municipality=self.instance.municipality)

            # Set initial values for pre-selected options on update
            self.initial['province'] = getattr(self.instance, 'province', None)
            self.initial['district'] = getattr(self.instance, 'district', None)
            self.initial['municipality'] = getattr(self.instance, 'municipality', None)
            # self.initial['area'] = getattr(self.instance, 'area', None)

        # Dynamically update queryset based on selections made during form submission
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

        # if 'municipality' in self.data:
        #     municipality_id = self.data.get('municipality')
        #     if municipality_id:
        #         self.fields['area'].queryset = Area.objects.filter(municipality_id=municipality_id)
        #     else:
        #         self.fields['area'].queryset = Area.objects.none()

class TeamForm(AddressMixin,forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name', 'total_players', 'sports_genere', 'short_name', 'is_organizers_team',
            'email', 'address', 'province', 'district', 'municipality', 'is_verified',
            'user', 'logo', 'banner', 'gender'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter team name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter contact email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter team address'}),
            'short_name': forms.TextInput(attrs={'placeholder': 'Enter short name'}),
            'total_players': forms.NumberInput(attrs={'min': 1, 'max': 50}),
        }


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




# address mixin


""" Event form"""
class EventForm(AddressMixin,forms.ModelForm):
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

    # Optional: You can add custom validation if needed
    def clean_entry_fee(self):
        fee = self.cleaned_data.get('entry_fee')
        if fee < 0:
            raise forms.ValidationError(_('Entry fee must be positive.'))
        return fee



class EventTeamForm(forms.ModelForm):
    class Meta:
        model = EventTeam
        fields = ['event', 'team', 'is_verified']
        widgets = {
            'is_verified': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
            # Capture the selected event if passed as an argument
            event = kwargs.pop('event', None)
            super().__init__(*args, **kwargs)
            
            # Filter out teams already registered for the selected event
            if event:
                registered_teams = EventTeam.objects.filter(event=event).values_list('team', flat=True)
                self.fields['team'].queryset = Team.objects.exclude(id__in=registered_teams)
            else:
                # Default to an empty queryset if no event is provided
                self.fields['team'].queryset = Team.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get("event")
        team = cleaned_data.get("team")

        # Check if this team is already registered for the specified event
        if event and team:
            existing_registration = EventTeam.objects.filter(event=event, team=team).exists()
            if existing_registration:
                raise ValidationError("This team has already been registered for this event.")
        
        return cleaned_data




class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter OTP'
    }))

    
class OTPRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        max_length=128, 
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    confirm_password = forms.CharField(
        max_length=128, 
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data




