from django.db import models
from sportsApp.models import Event,EventTeam,Player,Team
from datetime import datetime
from django.contrib.auth.models import User,Group
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
from sportsApp import constants
from datetime import timedelta
from django.utils.timezone import now
# Create your models here.
# Match Model
class Match(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,blank=True,null=True,related_name='matches')
    team1 = models.ForeignKey(EventTeam, on_delete=models.CASCADE, related_name='match_team1')
    team2 = models.ForeignKey(EventTeam, on_delete=models.CASCADE, related_name='match_team2')
    is_address_default = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=constants.MatchStatus.choices,default=constants.MatchStatus.INITIATED)
    match_date = models.DateField()
    match_time = models.TimeField(blank=True,null=True)
    place = models.CharField(max_length=255,blank=True,null=True)
    match_complete = models.BooleanField(default=False)
    notes = models.TextField(null=True,blank=True)
    schedule = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def match_day(self):
        day_of_week = self.match_date.strftime('%A')
        return day_of_week
    

    def clean(self) -> None:
        super().clean()
        if self.team1 == self.team2:
            raise ValidationError("Team 1 and Team2 Cannot be the same")
        
    
    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.match_date}"




class MatchTimeManager(models.Model):
    match = models.OneToOneField(
        'Match',
        on_delete=models.CASCADE,
        related_name='time_manager'
    )
    start_time = models.DateTimeField(blank=True,null=True)

    first_half_start_time = models.DateTimeField(blank=True,null=True)
    second_half_start_time = models.DateTimeField(blank=True,null=True)
    
    extra_time_first_half = models.DurationField(
        default=timedelta(0),
        blank=True,
        null=True, 
        help_text="Extra time added after the first half."
    )
    extra_time_full_time = models.DurationField(
        default=timedelta(0), 
        blank=True,
        null=True,
        help_text="Extra time added after the full-time duration."
    )

    match_ended = models.BooleanField(
        default=False, 
        help_text="Indicates whether the match has ended."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def match_status(self):
        """
        Determines the current status of the match.
        """
        if self.match_ended:
            return "Ended"
        if self.start_time is None:
            return "Not Started"
        # If there's a pause without a resume, the match is paused
        if self.match.pause_resume_sessions.filter(resumed_at__isnull=True).exists():
            return "Paused"
        return "Ongoing"

    def __str__(self):
        return f"Time Manager for Match {self.match.id} - Status: {self.match_status}"

class MatchPauseResume(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='pause_resume_sessions')
    paused_at = models.DateTimeField(help_text="The time when the match was paused.",default=now)
    resumed_at = models.DateTimeField(null=True, blank=True, help_text="The time when the match resumed.")
    is_before_half = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def duration(self):
        """
        Returns the duration of this pause if resumed.
        """
        if self.resumed_at:
            return self.resumed_at - self.paused_at
        return timedelta(0)

    def __str__(self):
        return f"Pause at {self.paused_at}, Resume at {self.resumed_at or 'Not Resumed'}"
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
    


    
class Refree(models.Model):
    REFREE_POSITION = (
        ('LEFT_TOUCH_LINE','Left Touch Line'),
        ('RIGHT_TOUCH_LINE','Right Touch Line'),
        ('MAIN','Main'),
        ('OUTSIDE','Outside')
    )
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event,on_delete=models.SET_NULL,blank=True,null=True)
    match = models.ForeignKey(Match,on_delete=models.SET_NULL,blank=True,null=True)
    position = models.CharField(max_length=100,choices=REFREE_POSITION)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    image = models.ImageField(upload_to='images/refree/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




# Models for Fall Goal
class Goal(models.Model):
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name='goals')
    goal_description = models.CharField(max_length=255,blank=True,null=True)
    goal_type = models.CharField(max_length=20,choices=constants.GOAL_TYPE.choices,default=constants.GOAL_TYPE.OPEN_PLAY)
    goal_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Fall(models.Model):
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name='fouls')
    fall_category = models.CharField(max_length=20,choices=constants.FoulCategory.choices,default=constants.FoulCategory.NORMAL_FALL)
    fall_type = models.CharField(max_length=20,choices=constants.FoulChoices.choices)
    fall_description = models.CharField(max_length=255,blank=True,null=True)
    fall_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Substitution(models.Model):
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    player_out = models.ForeignKey(Player, related_name='new_player_substitutions', on_delete=models.CASCADE)
    player_in = models.ForeignKey(Player, related_name='previous_player_substitutions', on_delete=models.CASCADE)
    time = models.TimeField(blank=True,null=True)
    is_emergency_substitution = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PlayerMatchEvents(models.Model):

    match = models.OneToOneField(Match,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    status_type = models.CharField(max_length=50,choices=constants.PlayerEventStatusType.choices)
    time = models.TimeField()
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



# Model For League Game

class Guest(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    is_event_guest = models.BooleanField(default=False)
    match = models.ForeignKey(Match,on_delete=models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
