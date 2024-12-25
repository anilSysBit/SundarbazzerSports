from rest_framework import serializers
from sportsApp.models import TeamRequest, Team, Event, EventOrganizer,EventTeam,Player
from matchApp.models import Match


from django.db import transaction, IntegrityError
from django.contrib.auth.models import User,Group
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from ..permissions import IsAnonymous,HasTeamGroupPermission,HasEventOrganizerGroupPermission
from .event_serializers import EventSmallSerializer,EventTeamSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..response import SuccessResponse,ErrorResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

class MatchListUserSerializer(serializers.ModelSerializer):
    event = EventSmallSerializer(required=False)
    team1 = EventTeamSerializer(required=False)
    team2 = EventTeamSerializer(required=False)
    class Meta:
        model = Match
        fields = ('id','event','status','place','team1','team2','match_date','match_time','notes','created_at','updated_at',)



class MatchCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Match
        fields = ('event','team1','team2','match_date','match_time','is_address_default','place','notes')

    def validate(self, data):
        is_address_default = data.get('is_address_default') or False
        place = data.get('place')


        if is_address_default is False and not place:
            raise serializers.ValidationError({"place": "This field is required when 'is_address_default' is False."})
        
                # Get event and teams
        event = data.get('event')
        team1 = data.get('team1')
        team2 = data.get('team2')
        match_date = data.get('match_date')

        # Check for existing matches for the same event
        if Match.objects.filter(
            Q(event=event, team1=team1, team2=team2, match_date=match_date) | 
            Q(event=event, team1=team1, team2=team2, match_date__gte=timezone.now())
        ).exists():

            raise serializers.ValidationError({
                'match': 'A match between these teams is already scheduled for this event.'
            })
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
            return SuccessResponse("Successfully Created a Match",serializers.data,status=status.HTTP_201_CREATED)
        else:
            return ErrorResponse("Some Error Occured",serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        




class UserListMatchViewSet(APIView):

    def get(self,request):
        match = Match.objects.all()
        serializer = MatchListUserSerializer(match,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)   

    


class MatchSingleViewSet(APIView):

    def get(self,request,pk):
        match = Match.objects.get(pk=pk)
        serializer = MatchListUserSerializer(match,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)   



class PlayerSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id","name","jersey_no","is_active")

class PlayerStatsSerializer(serializers.ModelSerializer):
    goal_count = serializers.IntegerField()
    foul_count = serializers.IntegerField()

    class Meta:
        model = Player
        fields = ['id', 'name','jersey_no','is_active', 'goal_count', 'foul_count']

    

class MatchTeamPlayersView(APIView):
    def get(self, request, match_id, team_id):
        match = get_object_or_404(Match, pk=match_id)

        # Determine the team (team1 or team2) based on the team_id
        if match.team1.team.id == team_id:
            team = match.team1.team
        elif match.team2.team.id == team_id:
            team = match.team2.team
        else:
            return Response({"error": "Team does not belong to the given match"}, status=400)

        # Fetch players of the specified team and annotate with goal and foul counts
        players = Player.objects.filter(team=team).annotate(
            goal_count=Count('goals', filter=Q(goals__match=match)),
            foul_count=Count('fouls', filter=Q(fouls__match=match))
        ).order_by('-is_active')

        total_goals = sum(player.goal_count for player in players)


        # Serialize player data
        serialized_players = PlayerStatsSerializer(players, many=True).data

        return Response({
            "id":team.id,
            "total_goals":total_goals,
            "team": team.name,
            "players": serialized_players
        })


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
