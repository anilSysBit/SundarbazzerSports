from rest_framework import serializers
from sportsApp.models import TeamRequest, Team, Event, EventOrganizer

from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404



class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = "__all__"