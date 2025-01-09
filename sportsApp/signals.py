from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchStatus,TieSheet
from team.models import Team,PointTable

@receiver(post_save, sender=MatchStatus)
def update_point_table(sender, instance, created, **kwargs):
    if instance.winner and created:
        # Increment total matches played for both teams via TieSheet
        instance.game.team1.total_match_played += 1
        instance.game.team1.save()

        instance.game.team2.total_match_played += 1
        instance.game.team2.save()

        point_table_winner = PointTable.objects.get(team=instance.winner)
        point_table_winner.points += 1
        point_table_winner.status = '3'
        point_table_winner.save()

@receiver(post_save, sender=MatchStatus)
def change_match_complete_on_tiesheet(sender, instance, created, **kwargs):
    if created:  # If a new MatchStatus instance is created
        team1 = instance.game.team1
        team2 = instance.game.team2
        tie_sheet = TieSheet.objects.get(team1=team1,team2=team2)
        tie_sheet.match_complete = True
        tie_sheet.save()
        
@receiver(post_save, sender=Team)
def create_point_table(sender, instance, created, **kwargs):
    if created:
        PointTable.objects.create(team=instance)


