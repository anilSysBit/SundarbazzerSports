from django.db import models
from datetime import datetime
from django.contrib.auth.models import User,Group
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from address.models import Province,District,Municipality
from team.models import Team
import uuid
from . import constants
from datetime import timedelta,datetime
# Create your models here.
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

    
class OTP(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        print(datetime.now())
        print(now())
        # return now() <= self.created_at + timedelta(minutes=5)
        return True
    
class TieSheet(models.Model):
    pass


class TeamRequest(models.Model):
    SPORT_TYPES = (
        ('FOOTBALL','Football'),    
    )
    name = models.CharField(max_length=255)
    short_name = models.CharField(unique=True,max_length=10,blank=True,null=True)
    # total_players = models.PositiveIntegerField(default=10)
    sports_genere = models.CharField(max_length=25,choices=SPORT_TYPES,default='FOOTBALL')
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    registration_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.name}'
    



class EventOrganizer(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='organizer')
    address = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    logo = models.ImageField(upload_to='images/events/',blank=True,null=True)
    banner = models.ImageField(upload_to='images/banner/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20,choices=constants.EVENT_TYPE.choices,default=constants.EVENT_TYPE.KNOCKOUT)
    status = models.CharField(max_length=20,choices=constants.EventStatus.choices,default=constants.EventStatus.INITIATED)
    banner = models.ImageField(upload_to='images/events/',blank=True,null=True)
    logo = models.ImageField(upload_to='images/events/',blank=True,null=True)
    event_organizer = models.ForeignKey(EventOrganizer,on_delete=models.CASCADE,blank=True,null=True,related_name='events')
    event_age_limit = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    entry_fee = models.DecimalField(max_digits=10000,decimal_places=3)
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    event_start_date = models.DateTimeField(blank=True,null=True)
    event_end_date = models.DateTimeField(blank=True,null=True)
    match_duration = models.DurationField(blank=True,null=True)
    
    # address

    province = models.ForeignKey(Province, on_delete=models.SET_NULL,null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL,null=True)
    area = models.CharField(max_length=255)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
class EventTeam(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team.name



class EventMemberRole(models.Model):
    name = models.CharField(max_length=50,unique=True)
    short_name = models.CharField(max_length=5,unique=True)
    description = models.TextField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class EventMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    organizer = models.ForeignKey(EventOrganizer,on_delete=models.CASCADE)
    role = models.ForeignKey(EventMemberRole,on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=6,decimal_places=3,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'${self.first_name} {self.last_name}'



class MatchStatus(models.Model):
    # game = models.ForeignKey(TieSheet,on_delete=models.CASCADE,null=True,blank=True)
    team1_point = models.PositiveIntegerField(default=0)
    team2_point = models.PositiveIntegerField(default=0)
    winner = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True,related_name='won_match')
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def calc_winner(self):
        team1_score = self.team1_point
        team2_score = self.team2_point

        if team1_score > team2_score:
            self.winner = self.game.team1
        elif team2_score > team1_score:
            self.winner = self.game.team2
        else:
            self.winner = None

        return self.winner
    

    def save(self, *args, **kwargs):
        self.calc_winner()  # Calculate the winner before saving
        super().save(*args, **kwargs)  # Call the original save method to save the object

    def __str__(self) -> str:
        return f"{self.winner} is the Winner of the Match of date:{self.game.match_date}"



# Recent Events

class RecentEvents(models.Model):
    SPORT_TYPES = (
        ('FOOTBALL','Football'),
    )
    date = models.DateField()
    event_title= models.CharField(max_length=255)
    event_description = models.TextField()
    sport_type = models.CharField(max_length=25,choices=SPORT_TYPES,default='FOOTBALL')
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.event_title
    



class LatestNews(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField()
    image = models.ImageField(upload_to="images/")
    text = models.TextField()
    created_at= models.DateField(auto_now_add=True,blank=True,null=True)

    def __str__(self) -> str:
        return ' '.join(self.text.split()[:10])
    
    def sm_text(self):
        return " ".join(self.text.split()[:10])
    







# Requesting before creating a event
class EventRequest(models.Model):
    requestor_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    event_budget = models.DecimalField(max_digits=10,decimal_places=10,blank=True,null=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)





# Event Members (Add Event Members)


class EventManagement(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)


class Sponser(models.Model):
    SPONSERS_TYPE = (
        ('PLATFORM_SPONSERS','platform'),
        ('EVENT_SPONSERS','event')
    )
    name = models.CharField(max_length=100)
    sponser_type = models.CharField(max_length=25,choices=SPONSERS_TYPE)
    event = models.ForeignKey(EventOrganizer,on_delete=models.PROTECT,null=True,blank=True)
    logo = models.ImageField(upload_to='images/sponsers/',blank=True,null=True)
    banner = models.ImageField(upload_to='images/sponsers/',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

    def clean(self):
        # Custom validation logic
        if self.sponser_type == 'EVENT_SPONSERS' and not self.event:
            raise ValidationError('Event must be selected if the sponsor type is "EVENT_SPONSERS".')
        elif self.sponser_type == 'PLATFORM_SPONSERS' and self.event:
            raise ValidationError('Event should not be selected if the sponsor type is "PLATFORM_SPONSERS".')

    def save(self, *args, **kwargs):
        # Call the clean method before saving
        self.clean()
        super(Sponser, self).save(*args, **kwargs)



# Models for the Platform


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
    

class Messages(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.email


class Payment(models.Model):
    TRANSACTION_TYPE = (
        ('EVENT_REGISTRATION_PAYMENT','event payment'),
        ('TEAM_REGISTRATION_PAYMENT','Team Registration payment'),
        ('EVENT_MEMBER_PAYMENT','Event Member Payment'),
        ('WIN_TEAM_PAYMENT','Winning Team Payment'),
        ('PLAYER_PAYMENT','PLAYER PAYMENT'),
        ('OTHERS','others')
    )
    transaction_type = models.CharField(max_length=50,choices=TRANSACTION_TYPE)
    transaction_uuid = models.CharField(max_length=255,unique=True,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    status = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_uuid  = models.CharField(max_length=255,unique=True)
    product_code = models.CharField(max_length=255)
    ref_id = models.CharField(max_length=255)
    payment = models.ForeignKey(Payment,on_delete=models.RESTRICT,null=True,blank=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

