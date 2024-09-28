from rest_framework import serializers
from sportsApp.models import TeamRequest, Team, Event, EventOrganizer,Match,EventTeam

from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from ..permissions import IsAnonymous,HasTeamGroupPermission,HasEventOrganizerGroupPermission
from .event_serializers import EventSmallSerializer,EventTeamSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class MatchListUserSerializer(serializers.ModelSerializer):
    event = EventSmallSerializer(required=False)
    team1 = EventTeamSerializer(required=False)
    team2 = EventTeamSerializer(required=False)
    class Meta:
        model = Match
        fields = ('id','event','place','team1','team2','match_date','notes','created_at','updated_at',)



class MatchCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Match
        fields = ('event','team1','team2','match_date','is_address_default','place','notes')

    def validate(self, data):
        is_address_default = data.get('is_address_default') or False
        place = data.get('place')


        if is_address_default is False and not place:
            raise serializers.ValidationError({"place": "This field is required when 'is_address_default' is False."})
        
        return data


class MatchViewSet(APIView):
    permission_classes = [HasEventOrganizerGroupPermission]

    def post(self,request,*args,**kwargs):

        event_id = kwargs.get('event_id')


        try:
            event = Event.objects.get(pk = event_id,event_organizer__user=request.user)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or you do not have permission to access this event"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['event'] = event.id

        serializers = MatchCreateSerializer(data=data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        


 
class UserListMatchViewSet(APIView):

    def get(self,request):
        match = Match.objects.all()
        serializer = MatchListUserSerializer(match,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)   