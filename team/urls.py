from django.urls import path,include
from . import views
from django.conf import settings
from sportsApp.views import create_team_view
from .views import register_team,team_success_view

urlpatterns = [
    path('team-registration/<uuid:res_id>/',register_team,name='team_resistration'),
    path('team-registration/success/',team_success_view,name='team_registration_success')
]