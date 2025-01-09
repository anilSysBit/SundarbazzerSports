from django.urls import path,include
from . import views
from django.conf import settings
from sportsApp.views import create_team_view

urlpatterns = [
    path('create',create_team_view,name='team_create_team')
]