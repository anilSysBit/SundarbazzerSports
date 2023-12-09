from django.db import models
from datetime import datetime
# Create your models here.

class Team(models.Model):
    team_code = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    total_players = models.PositiveIntegerField(default=10)
    total_match_played = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.name}'


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
        ('NATIONAL','National'),
        ('FOOTBALL','Football'),
        ('VOLLEYBALL','Volleyball'),
        ('TENNIS','Tennis'),
        ('GLOBAL','Global'),
        ('CIRCKET','Circket')
    )
    date = models.DateField()
    event_title= models.CharField(max_length=255)
    event_description = models.TextField()
    sport_type = models.CharField(max_length=25,choices=SPORT_TYPES,default='NATIONAL')


    def __str__(self) -> str:
        return self.event_title
    

