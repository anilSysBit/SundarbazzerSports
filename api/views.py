from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from sportsApp.models import TeamRequest,Team
from .serializers.team_serializers import TeamRequestSerializer,TeamSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .permissions import IsAnonymous,HasTeamGroupPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

    def get_queryset(self):
        return Team.objects.filter(is_verified = True)
    
    def create(self, request, *args, **kwargs):
        return Response({'detail':'Method not allowed to post'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    
    @action(detail=False, methods=['post'])
    def custom_action(self, request,*args,**kwargs):
        # Your custom logic here
        request_id = kwargs.get('request_id')

        data = request.data.copy()
        team_request = TeamRequest.objects.filter(registration_number=request_id)
        data['request_id'] = request_id
        if not team_request.exists():
            return Response({'detail': 'Invalid request_id.'}, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        team_request.delete()
        headers = self.get_success_headers(serializer.data)
        return Response({'message':"Team Has Been Successfully Created"}, status=status.HTTP_201_CREATED, headers=headers)