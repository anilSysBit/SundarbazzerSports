from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from sportsApp.models import TeamRequest,Team
from .serializers.team_serializers import TeamRequestSerializer,TeamSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .permissions import IsAnonymous

class TeamRequestViewSet(ModelViewSet):
    # http_method_names = ['post']
    queryset = TeamRequest.objects.all()
    serializer_class = TeamRequestSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAnonymous()]
        return [IsAdminUser()]

    
class TeamViewSet(ModelViewSet):
    # queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Team.objects.filter(is_verified = True)