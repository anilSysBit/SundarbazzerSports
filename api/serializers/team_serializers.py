from rest_framework import serializers
from sportsApp.models import TeamRequest, Team

from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404

class TeamRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequest
        fields = '__all__'  # Include all fields in the serializer


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        # fields = "__all__"
        exclude = ['user']

    
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