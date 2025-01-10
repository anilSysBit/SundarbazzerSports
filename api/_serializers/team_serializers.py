from rest_framework import serializers
from team.models import  Team,Player
from sportsApp.models import TeamRequest
from matchApp.models import Match


from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# rest framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




class TeamRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequest
        fields = '__all__'  # Include all fields in the serializer



class TeamSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['id','name','short_name','email','address','logo','banner','gender']


    def get_logo(self, obj):
        # Return the full URL for the logo field
        if obj.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.logo.url)
        return None

    def get_banner(self, obj):
        # Return the full URL for the banner field
        if obj.banner:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.banner.url)
        return None

    
    def create(self, validated_data):
        with transaction.atomic():
            email = validated_data.get('email')
            username = email.split('@')[0]
            user = User.objects.create(
                username=username,
                email=email,
                is_staff=True,
            )
            group, created = Group.objects.get_or_create(name='TeamGroup')  # Replace 'TeamGroup' with your group name
            user.groups.add(group)
            # Set a random password
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            team = Team.objects.create(user=user,**validated_data)

            send_mail(
                subject="New Team Created Successfully",
                message=f'Team {team.name} has been successfully created. Username - {username} Email - {email} Password - {password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email,],
                fail_silently=False
            )
        return team
    

class TeamSmallSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    total_players = serializers.SerializerMethodField()

    """Serializer for the Team data."""
    class Meta:
        model = Team
        fields = ['id', 'name', 'address','is_verified', 'logo', 'banner','total_players']  # Add any other necessary team fields
        


    def get_total_players(self, obj):
            # Count the total number of players in the team
            return Player.objects.filter(team=obj).count()

    def get_logo(self, obj):
        # Return the full URL for the logo field
        if obj.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.logo.url)
        return None

    def get_banner(self, obj):
        # Return the full URL for the banner field
        if obj.banner:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.banner.url)
        return None

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Add other fields as needed



class TeamPlayerViewSet(APIView):
    
    def get(self,request,team_id):
        team = get_object_or_404(Team,pk=team_id)
        players = Player.objects.filter(team=team).order_by('-is_active')

        data = {
            'team':team,
            'players':players
        }
        serializer = TeamWithPlayersSerializer(data,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class TeamPlayersSerializer(serializers.ModelSerializer):
    position_display = serializers.SerializerMethodField()
    class Meta:
        model = Player
        fields = ['id','name','designation','position_display','jersey_no','is_active','is_playing','team']

    def get_position_display(self, obj):
        return obj.get_designation_display()

class TeamWithPlayersSerializer(serializers.Serializer):
    team = TeamSmallSerializer()
    players = TeamPlayersSerializer(many=True)


class TeamListViewSet(APIView):
        
        def get(self,request):
            teams = Team.objects.all()
            serializer = TeamSmallSerializer(teams,many=True,context={'request':request,'exclude':['logo']})
            return Response(serializer.data,status=status.HTTP_200_OK)