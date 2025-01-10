from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import generics
from sportsApp.models import TeamRequest,Event, EventOrganizer
from team.models import Team,Player
from matchApp.models import Match
from ._serializers.team_serializers import TeamRequestSerializer,TeamSerializer,UserProfileSerializer
from django.contrib.auth.models import User
from ._serializers.event_serializers import EventListSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .permissions import IsAnonymous,HasTeamGroupPermission,HasEventOrganizerGroupPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.decorators import permission_classes

class TeamRequestViewSet(APIView):

    

    def post(self, request, *args, **kwargs):
        # Deserialize the request data
        serializer = TeamRequestSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Check if the email exists in User model
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({'email': 'Email Address already in use'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the TeamRequest instance
            serializer.save()

            # Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(ModelViewSet):
    pass

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class TeamProfileAPIView(APIView):
    permission_classes = [HasTeamGroupPermission,IsAuthenticated]

    def get(self,request):
        user= request.user

        if not hasattr(user, 'team'):
            return Response({'detail': 'No team associated with this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        team = user.team

        serializer = TeamSerializer(team, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)



    def patch(self,request):
        user = request.user
        team = user.team
        print('Team',team)

        serializer = TeamSerializer(team, data=request.data,context={'request':request},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class EventUserViewSet(APIView):
    def get(self,request):
       events = Event.objects.all()
       serializer = EventListSerializer(events,many=True,context={'request':request})
       return Response(serializer.data,status=status.HTTP_200_OK)








