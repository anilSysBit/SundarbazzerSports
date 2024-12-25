from rest_framework import serializers
from sportsApp.models import TeamRequest, Team, Event, EventOrganizer,EventTeam
from matchApp.models import Match

from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api._serializers.serializers import ProvinceSerializer,DistrictSerializer,MunicipalitySerializer

class EventListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    organizer_name = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    # logo = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id','title','event_type','banner','event_age_limit','entry_fee','organizer_name','registration_start_date','email','phone','registration_end_date','event_start_date','event_end_date','is_verified','created_at','updated_at']
        read_only_fields = ['created_at','updated_at']

 # Method to get email from the EventOrganizer model
    def get_email(self, obj):
        return obj.event_organizer.user.email if obj.event_organizer else None

    # Method to get phone from the EventOrganizer model
    def get_phone(self, obj):
        return obj.event_organizer.phone if obj.event_organizer else None
    
     # Method to get email from the EventOrganizer model
    def get_organizer_name(self, obj):
        return obj.event_organizer.name if obj.event_organizer else None

    def get_banner(self, obj):
        # Return the full URL for the banner field
        if obj.banner:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.banner.url)
        return None




class EventSmallSerializer(serializers.ModelSerializer):
    default_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ('title','default_address','match_duration')
    
    def get_default_address(self, instance):
        # Combine the names of related fields to form the address string
        province = instance.province.name if instance.province else ''
        district = instance.district.name if instance.district else ''
        municipality = instance.municipality.name if instance.municipality else ''
        area = instance.area if instance.area else ''
        
        # Create a formatted address string, joining the fields with a comma
        address_parts = [province, district, municipality, area]
        return ', '.join(filter(None, address_parts))  # Remove 


class TeamSmallSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ("id","name","address","gender","short_name","logo")

    def get_logo(self, obj):
        # Return the full URL for the banner field
        if obj.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.logo.url)
        return None



class EventTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTeam
        fields = ('id',)
    
    def to_representation(self, instance):
        data= super().to_representation(instance)
        return TeamSmallSerializer(instance.team,context={'request':self.context.get('request')}).data


class EventViewDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTeam
        fields = ('id',)


class EventSerializer(serializers.ModelSerializer):
    event_teams = serializers.SerializerMethodField()
    province = ProvinceSerializer()
    district = DistrictSerializer()
    municipality = MunicipalitySerializer()

    logo = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'event_type', 'status', 'banner', 'logo',
            'event_organizer', 'event_age_limit', 'is_verified',
            'entry_fee', 'registration_start_date', 'registration_end_date',
            'event_start_date', 'event_end_date', 'match_duration',
            'province', 'district', 'municipality', 'area', 'created_at', 'updated_at',
            'event_teams'
        ]

    def get_event_teams(self, obj):
        teams = obj.eventteam_set.all()  # Reverse relation to get EventTeam objects
        return EventTeamSerializer(teams, many=True, context=self.context).data

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


class EventDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)