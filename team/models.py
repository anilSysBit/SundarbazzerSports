from django.db import models
from datetime import datetime
from django.contrib.auth.models import User,Group
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from address.models import Province,District,Municipality
import uuid
from sportsApp import constants
from datetime import timedelta,datetime
# Create your models here.
from django.utils.timezone import now

# Create your models here.
class Team(models.Model):
    SPORT_TYPES = (
        ('FOOTBALL','Football'),
    )

    name = models.CharField(max_length=255,db_index=1)
    total_players = models.PositiveIntegerField(default=10,blank=True, null=True)
    sports_genere = models.CharField(max_length=25,choices=SPORT_TYPES,default='FOOTBALL',blank=True)
    short_name = models.CharField(unique=True,max_length=10,blank=True,null=True)
    is_organizers_team = models.BooleanField(default=False)
    email = models.EmailField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)

    # address

    province = models.ForeignKey(Province, on_delete=models.SET_NULL,null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL,null=True)

    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='team')
    logo = models.ImageField(upload_to="images/teams/",blank=True,null=True)
    banner = models.ImageField(upload_to='images/banner/',blank=True,null=True)
    gender = models.CharField(max_length=25,choices=constants.GENDER_OPTIONS.CHOICES,default=constants.GENDER_OPTIONS.MALE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
class TeamOwner(models.Model):
    team = models.OneToOneField(Team,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(max_length=100,blank=True,null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='images/teams/owner/', blank=True, null=True)
    descrption = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TeamDesign(models.Model):
    team = models.OneToOneField(Team,on_delete=models.CASCADE)
    primary_color = models.CharField(max_length=100,blank=True,null=True)
    secondary_color = models.CharField(max_length=100,blank=True,null=True)
    jersey_number_color = models.CharField(max_length=100,blank=True,null=True)
    neckline_color=models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

class PointTable(models.Model):
    PENDING = 'Pending'
    STATUS_CHOICES = (
        ('PENDING','Pending'),
        ('IN_MATCH','In Match'),
        ('ELIMINATED','Eliminated')
    )
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20,choices = STATUS_CHOICES,default='PENDING')



class Player(models.Model):

    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    jersey_no = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    weight = models.PositiveIntegerField(blank=True,null=True)
    is_active = models.BooleanField(default=False)
    is_playing = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='images/teams/', blank=True, null=True)
    height = models.PositiveIntegerField(blank=True,null=True)
    blood_group = models.CharField(max_length=25, choices=constants.BLOOD_GROUPS.choices)
    address = models.TextField(blank=True,null=True)
    designation = models.CharField(max_length=100, choices=constants.PLAYER_POSITION.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({self.jersey_no}) - {self.team}"

    def clean(self):
        # Check if another player in the same team has the same jersey number
        if Player.objects.filter(team=self.team, jersey_no=self.jersey_no).exclude(pk=self.pk).exists():
            raise ValidationError({'jersey_no':f"A player with jersey number {self.jersey_no} already exists in team {self.team}."})

    def save(self, *args, **kwargs):
            self.clean()  # Call the clean method to enforce validation
            super().save(*args, **kwargs)
# Model for the event


class TeamStatus(models.Model):
    team = models.OneToOneField(Team,on_delete=models.PROTECT)
    total_match_played = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)



class Coach(models.Model):
    team = models.OneToOneField(Team,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(max_length=100,blank=True,null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='images/coach/')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
