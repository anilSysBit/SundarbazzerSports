from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import generics
from sportsApp.models import TeamRequest,Team,Event, EventOrganizer,Match
from .serializers.team_serializers import TeamRequestSerializer,TeamSerializer,UserProfileSerializer
from django.contrib.auth.models import User
from .serializers.event_serializers import EventListSerializer, EventOrganizerSerializer,OrganizerEventListSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .permissions import IsAnonymous,HasTeamGroupPermission,HasEventOrganizerGroupPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.decorators import permission_classes

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

    permission_classes = [IsAuthenticated]

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
    

class EventProfileApiView(APIView):
    permission_classes= []

    # @permission_classes([IsAuthenticated])

    def get(self,request):
        user= request.user

        if not hasattr(user, 'organizer'):
            return Response({'detail': 'No organizer associated with this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        organizer = user.organizer

        serializer = EventOrganizerSerializer(organizer, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer = EventOrganizerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class EventUserViewSet(APIView):
    def get(self,request):
       events = Event.objects.all()
       serializer = EventListSerializer(events,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)



class OrganizerEventViewSet(APIView):

    permission_classes =[HasEventOrganizerGroupPermission]


    def get(self,request):
        user = request.user

        if not hasattr(user, 'organizer'):
            return Response({'detail': 'You are not an organizer'}, status=status.HTTP_404_NOT_FOUND)

        organizer = user.organizer

        events = Event.objects.filter(event_organizer=organizer)

        serializer = OrganizerEventListSerializer(events,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    


