from django.urls import path,include
from . import views
from django.conf import settings
from sportsApp.views import create_team_view
from .views import register_team,team_success_view,edit_team_profile,team_players,team_ongoing_events_view,team_jersey_view

urlpatterns = [
    path('team-registration/<uuid:res_id>/',register_team,name='team_resistration'),
    path('team-registration/success/',team_success_view,name='team_registration_success'),
    path('profile/',edit_team_profile,name='team_profile'),
    path('team-players',team_players,name='team-players'),
    path('ongoing-events',team_ongoing_events_view,name='team_ongoing_events'),
    path('team-jersey',team_jersey_view,name='team_jersey'),
]