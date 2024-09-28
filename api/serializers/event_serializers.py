from rest_framework import serializers
from sportsApp.models import TeamRequest, Team, Event, EventOrganizer,Match,EventTeam

from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404



class EventListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    organizer_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['title','event_type','banner','event_age_limit','entry_fee','organizer_name','registration_start_date','email','phone','resistration_end_date','event_start_date','event_end_date','is_verified','created_at','updated_at']
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


class OrganizerEventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title','event_type','banner','event_age_limit','entry_fee','registration_start_date','resistration_end_date','event_start_date','event_end_date','is_verified','created_at','updated_at']
        read_only_fields = ['created_at','updated_at']

class EventOrganizerSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    user_email = serializers.ReadOnlyField(source='user.email')  # Include user's email
    class Meta:
        model = EventOrganizer
        fields = ['name', 'email', 'password', 'address', 'logo', 'banner', 'created_at', 'updated_at','user_email']
        read_only_fields = ['user_email','created_at', 'updated_at']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        try:
            # Using a transaction to ensure all operations happen together
            with transaction.atomic():
                # Create the User instance (Django will enforce unique email)
                user = User.objects.create_user(username=email, email=email, password=password,is_staff=True)

                # Get or create the 'EventOrganizer' group
                event_organizer_group, created = Group.objects.get_or_create(name='EventOrganizer')

                # Add the user to the 'EventOrganizer' group
                user.groups.add(event_organizer_group)

                # Create the EventOrganizer instance and associate it with the created user
                event_organizer = EventOrganizer.objects.create(user=user, **validated_data)

                return event_organizer

        except IntegrityError:
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})


class EventSmallSerializer(serializers.ModelSerializer):
    organizer_name = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ('title','organizer_name')

        # Method to get email from the EventOrganizer model
    def get_organizer_name(self, obj):
        return obj.event_organizer.name if obj.event_organizer else None
    

class TeamSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id","name","address","gender","short_name",)


class EventTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTeam
        fields = ('id',)
    
    def to_representation(self, instance):
        data= super().to_representation(instance)
        return TeamSmallSerializer(instance.team).data

