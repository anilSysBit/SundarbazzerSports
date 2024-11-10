from django.db import models
from datetime import datetime
from django.contrib.auth.models import User,Group
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
from . import constants
# Create your models here.

class TeamRequest(models.Model):
    SPORT_TYPES = (
        ('FOOTBALL','Football'),    
    )
    name = models.CharField(max_length=255)
    short_name = models.CharField(unique=True,max_length=10,blank=True,null=True)
    total_players = models.PositiveIntegerField(default=10)
    sports_genere = models.CharField(max_length=25,choices=SPORT_TYPES,default='FOOTBALL')
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    registration_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.name}'
    

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
    address = models.CharField(max_length=255,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='team')
    logo = models.ImageField(upload_to="images/teams/",blank=True,null=True)
    banner = models.ImageField(upload_to='images/banner/',blank=True,null=True)
    gender = models.CharField(max_length=25,choices=constants.GENDER_OPTIONS.CHOICES,blank=True,null=True)
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



class TieSheet(models.Model):

 pass


class Player(models.Model):

    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    jersey_no = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    weight = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='images/teams/', blank=True, null=True)
    height = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=25, choices=constants.BLOOD_GROUPS.choices)
    address = models.TextField(blank=True,null=True)
    designation = models.CharField(max_length=100, choices=constants.PLAYER_POSITION.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({self.jersey_no}) - {self.team}"

# Model for the event

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
    EVENT_TYPE = (
        ('LEAGUE','League'),
        ('KNOCKOUT','Knockout'),
        ('FRIENDLY','Friendly')
    )

    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20,choices=EVENT_TYPE,blank=True,null=True)
    banner = models.ImageField(upload_to='images/events/',blank=True,null=True)
    event_organizer = models.ForeignKey(EventOrganizer,on_delete=models.CASCADE,blank=True,null=True,related_name='events')
    event_age_limit = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    entry_fee = models.DecimalField(max_digits=10000,decimal_places=3)
    registration_start_date = models.DateField()
    resistration_end_date = models.DateField()
    event_start_date = models.DateField(blank=True,null=True)
    event_end_date = models.DateField(blank=True,null=True)
    match_duration = models.DurationField(blank=True,null=True)
    default_address = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
class EventTeam(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team.name

# Match Model
class Match(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,blank=True,null=True,related_name='matches')
    team1 = models.ForeignKey(EventTeam, on_delete=models.CASCADE, related_name='match_team1')
    team2 = models.ForeignKey(EventTeam, on_delete=models.CASCADE, related_name='match_team2')
    is_address_default = models.BooleanField(default=False)
    match_date = models.DateField()
    match_time = models.TimeField(blank=True,null=True)
    place = models.CharField(max_length=255,blank=True,null=True)
    match_complete = models.BooleanField(default=False)
    notes = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def match_day(self):
        day_of_week = self.match_date.strftime('%A')
        return day_of_week
    

    def clean(self) -> None:
        super().clean()

        if self.team1 == self.team2:
            raise ValidationError("Team 1 and Team2 Cannot be the same")
        
        if not self.team1.event == self.event:
            raise ValidationError("Team1 Should be of the Same Event")
        if not self.team2.event == self.event:
            raise ValidationError("Team2 Should be of the Same Event")
    
    def save(self, *args, **kwargs):
        # Ensure clean is called when saving
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.match_date}"


# class MatchPlayers(models.Model):
#     match = models.ForeignKey(Match,on_delete=models.CASCADE)
#     player = models.ForeignKey(Player,on_delete=models.CASCADE)
#     designation = models.CharField(max_length=50,choices=constants.PLAYER_POSITION.choices)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

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

    
class Refree(models.Model):
    REFREE_POSITION = (
        ('LEFT_TOUCH_LINE','Left Touch Line'),
        ('RIGHT_TOUCH_LINE','Right Touch Line'),
        ('MAIN','Main'),
        ('OUTSIDE','Outside')
    )
    name = models.CharField(max_length=100)
    event = models.ForeignKey('Event',on_delete=models.SET_NULL,blank=True,null=True)
    match = models.ForeignKey(Match,on_delete=models.SET_NULL,blank=True,null=True)
    position = models.CharField(max_length=100,choices=REFREE_POSITION)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    image = models.ImageField(upload_to='images/refree/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Match Interruption Model

class MatchInterruption(models.Model):
    INTERRUPTIONS_CAUSES = [
        ('weather', 'Weather Conditions'),
        ('injury', 'Player Injury'),
        ('equipment', 'Equipment Failure'),
        ('crowd', 'Crowd Disturbance'),
        ('technical', 'Technical Issue'),
        ('other', 'Other'),
    ]
    interrupted_date = models.DateTimeField()
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    cause = models.CharField(max_length=50, choices=INTERRUPTIONS_CAUSES)
    duration = models.DateTimeField()
    resumed_date = models.DateTimeField(null=True,blank=True)
    severity = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    # reported_by = models.CharField(max_length=100)
    notes = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return f"Interruption on {self.interrupted_date} for match {self.match}"
    


# Models for Fall Goal
class Goal(models.Model):
    match = models.OneToOneField(Match,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    goal_description = models.CharField(max_length=255)
    goal_type = models.CharField(max_length=20,choices=constants.GOAL_TYPE.choices,default=constants.GOAL_TYPE.OPEN_PLAY)
    goal_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()

        if self.team not in [self.match.team1,self.match.team2]:
            raise ValidationError('The Selected Team Must be one of the Teams playing in the Match')
        
        if self.player.team != self.team:
            raise ValidationError('The Selected Player must be on the Selected Team')
        
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)


class Fall(models.Model):

    FALL_TYPE = (
        ('NORMAL','Normal'),
        ('RED_CARD','Red Card'),
        ('YELLOW_CARD','Yellow Card')
    )
    
    match = models.OneToOneField(Match,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)

    fall_type = models.CharField(max_length=20,choices=FALL_TYPE)
    fall_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()

        if self.team not in [self.match.team1,self.match.team2]:
            raise ValidationError('The Selected Team Must be one of the Teams playing in the Match')
        
        if self.player.team != self.team:
            raise ValidationError('The Selected Player must be on the Selected Team')
        
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)
    
class Substitution(models.Model):
    match = models.OneToOneField(Match,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    new_player = models.ForeignKey(Player, related_name='new_player_substitutions', on_delete=models.CASCADE)
    previous_player = models.ForeignKey(Player, related_name='previous_player_substitutions', on_delete=models.CASCADE)
    is_emergency_substitution = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.team not in [self.match.team1,self.match.team2]:
            raise ValidationError('The Selected Team Must be one of the Teams playing in the Match')
        
        if (self.player.team != self.team) or (self.new_player.team != self.team):
            raise ValidationError('The Selected Player must be on the Selected Team')
        
        if(self.new_player  == self.previous_player):
            raise ValidationError('Same Player Cannot be substituted')
        
        
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)

class PlayerMatchEvents(models.Model):

    STATUS_TYPE = (
        ('FREEKICK','FreeKick'),
        ('CORNER','Corner'),
        ('PENALTY','Penalty'),
        ('OFFSIDE','Offside'),
        ('INJURY','Injury')
        
    )
    match = models.OneToOneField(Match,on_delete=models.CASCADE)
    player = models.ForeignKey('Player',on_delete=models.CASCADE)
    status_type = models.CharField(max_length=50,choices=STATUS_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.team not in [self.match.team1,self.match.team2]:
            raise ValidationError('The Selected Team Must be one of the Teams playing in the Match')
        
        if self.player.team != self.team:
            raise ValidationError('The Selected Player must be on the Selected Team')
        
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)



class MatchStatus(models.Model):
    game = models.ForeignKey(TieSheet,on_delete=models.CASCADE,null=True,blank=True)
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



class TeamStatus(models.Model):
    team = models.OneToOneField(Team,on_delete=models.PROTECT)
    total_match_played = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)


# Requesting before creating a event
class EventRequest(models.Model):
    requestor_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    event_budget = models.DecimalField(max_digits=10,decimal_places=10,blank=True,null=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)




# Model For League Game

class Guest(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    is_event_guest = models.BooleanField(default=False)
    match = models.ForeignKey(Match,on_delete=models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    