# matchApp/tasks.py
from celery import shared_task
from matchApp.models import Match
from django.utils.timezone import make_aware, now  # Use Django's timezone utilities
from datetime import datetime
from . import constants

@shared_task
def update_match_status(match_id):
    """
    Update match status to 'EXPIRED' if the match date and time have passed.
    """
    try:
        match = Match.objects.get(id=match_id)
        match_datetime = make_aware(datetime.combine(match.match_date, match.match_time))  # Convert to timezone-aware
        if now() > match_datetime:
            match.match_status = constants.MatchStatus.EXPIRED  # Update status
            match.save()
            print(f"Updated match {match.id} to EXPIRED")
        else:
            print(f"Match {match.id} is still in the future.")
    except Match.DoesNotExist:
        print(f"Match with ID {match_id} does not exist.")
