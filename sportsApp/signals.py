from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchStatus,PointTable

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
        point_table_winner.status = 'IN_MATCH'
        point_table_winner.save()

        
