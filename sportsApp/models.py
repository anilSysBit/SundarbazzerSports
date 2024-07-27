from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
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
    created_at = models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.name}'
    
class Team(models.Model):
    SPORT_TYPES = (
        ('FOOTBALL','Football'),
    )
    GENDER = (
        ("MALE","male"),
        ('FEMALE','female'),
    )
    name = models.CharField(max_length=255, blank=True)
    total_players = models.PositiveIntegerField(blank=True, null=True)
    sports_genere = models.CharField(max_length=25,choices=SPORT_TYPES,default='FOOTBALL',blank=True)
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    logo = models.ImageField(upload_to="images/teams/",blank=True,null=True)
    banner = models.ImageField(upload_to='images/banner/',blank=True,null=True)
    gender = models.CharField(max_length=25,blank=True,null=True)
    created_at = models.DateField(blank=True, null=True,auto_now_add=True)
    updated_at = models.DateField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.pk and self.email:
            # Generate a random username
            username = self.email.split('@')[0] + get_random_string(5)
            
            # Create the user instance
            user = User.objects.create(
                username=username,
                email=self.email
            )
            
            # Set a random password
            password = User.objects.make_random_password()
            user.set_password(password)
            
            # Send email with credentials
            self._send_email(username, self.email, password)

            user.save()

            # Associate the user with the team
            self.user = user

        super().save(*args, **kwargs)
    
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
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    match_date = models.DateField()
    place = models.CharField(max_length=255)
    match_complete = models.BooleanField(default=False)

    def match_day(self):
        day_of_week = self.match_date.strftime('%A')
        return day_of_week
    
    def __str__(self) -> str:
        return f"{self.team1.team_code} vs {self.team2.team_code}"
    

class MatchStatus(models.Model):
    game = models.ForeignKey(TieSheet,on_delete=models.CASCADE,null=True,blank=True)
    team1_point = models.PositiveIntegerField(default=0)
    team2_point = models.PositiveIntegerField(default=0)
    winner = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True,related_name='won_match')

    
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
    

class Player(models.Model):
    BLOOD_GROUPS = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-')
    )
        # Define choices for football positions
    GOALKEEPER = 'GK'
    RIGHT_BACK = 'RB'
    LEFT_BACK = 'LB'
    CENTER_BACK = 'CB'
    DEFENSIVE_MIDFIELDER = 'DM'
    CENTRAL_MIDFIELDER = 'CM'
    ATTACKING_MIDFIELDER = 'AM'
    RIGHT_MIDFIELDER = 'RM'
    LEFT_MIDFIELDER = 'LM'
    RIGHT_WINGER = 'RW'
    LEFT_WINGER = 'LW'
    FORWARD = 'FW'
    STRIKER = 'ST'

    POSITION_CHOICES = [
        (GOALKEEPER, 'Goalkeeper'),
        (RIGHT_BACK, 'Right Back'),
        (LEFT_BACK, 'Left Back'),
        (CENTER_BACK, 'Center Back'),
        (DEFENSIVE_MIDFIELDER, 'Defensive Midfielder'),
        (CENTRAL_MIDFIELDER, 'Central Midfielder'),
        (ATTACKING_MIDFIELDER, 'Attacking Midfielder'),
        (RIGHT_MIDFIELDER, 'Right Midfielder'),
        (LEFT_MIDFIELDER, 'Left Midfielder'),
        (RIGHT_WINGER, 'Right Winger'),
        (LEFT_WINGER, 'Left Winger'),
        (FORWARD, 'Forward'),
        (STRIKER, 'Striker'),
    ]
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    jersey_no = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    profile_image = models.ImageField(upload_to='images/teams/',blank=True,null=True)
    # height stored in cm
    height = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=25,choices=BLOOD_GROUPS)
    address = models.TextField()
    designation = models.CharField(max_length=100,choices=POSITION_CHOICES,blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'jersey_no'], name='unique_jersey_no_per_team')
        ]
    def __str__(self):
        return f"{self.name} ({self.jersey_no}) - {self.team}"
    

class Coach(models.Model):
    team = models.OneToOneField(Team,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/coach/')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name



class TeamStatus(models.Model):
    team = models.OneToOneField(Team,on_delete=models.PROTECT)
    total_match_played = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)


class PlayerStatus(models.Model):
    player = models.OneToOneField(Player,on_delete=models.PROTECT)
    total_match_played = models.PositiveIntegerField()
    total_goals = models.PositiveIntegerField()
    total_man_of_the_match = models.PositiveIntegerField()




class Event(models.Model):
    banner = models.ImageField(upload_to='images/events/',blank=True,null=True)
    title = models.CharField(max_length=255)
    event_age_limit = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    entry_fee = models.DecimalField(max_digits=10000,decimal_places=3)
    registration_start_date = models.DateField()
    resistration_end_date = models.DateField()
    event_start_date = models.DateTimeField(blank=True,null=True)
    event_end_date = models.DateTimeField(blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title


class Sponser(models.Model):
    SPONSERS_TYPE = (
        ('PLATFORM_SPONSERS',1),
        ('EVENT_SPONSERS',2)
    )
    name = models.CharField(max_length=100)
    sponser_type = models.CharField(max_length=25,choices=SPONSERS_TYPE)
    event = models.ForeignKey(Event,on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='images/sponsers/',blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
    

class Messages(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email



