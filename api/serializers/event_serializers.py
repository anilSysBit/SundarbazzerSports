from rest_framework import serializers
from sportsApp.models import TeamRequest, Team, Event, EventOrganizer

from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404



class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


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