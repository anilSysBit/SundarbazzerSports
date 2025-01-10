from django.urls import path,include
from . import views
from django.conf import settings
from sportsApp.views import create_team_view
from .views import register_team,team_success_view,edit_team_profile

urlpatterns = [
    path('team-registration/<uuid:res_id>/',register_team,name='team_resistration'),
    path('team-registration/success/',team_success_view,name='team_registration_success'),
    path('profile/',edit_team_profile,name='team_profile'),
]