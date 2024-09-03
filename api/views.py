from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from sportsApp.models import TeamRequest,Team
from .serializers.team_serializers import TeamRequestSerializer,TeamSerializer

class TeamRequestViewSet(ModelViewSet):
    queryset = TeamRequest.objects.all()
    serializer_class = TeamRequestSerializer
    

    
class TeamViewSet(ModelViewSet):
    # queryset = Team.objects.all()

    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.filter(is_verified = True)