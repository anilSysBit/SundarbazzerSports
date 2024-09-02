from rest_framework import serializers
from sportsApp.models import TeamRequest, Team

class TeamRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequest
        fields = '__all__'  # Include all fields in the serializer


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        # fields = "__all__"
        exclude = ['user']