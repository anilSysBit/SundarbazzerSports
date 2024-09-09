from rest_framework import serializers
from sportsApp.models import TeamRequest, Team

from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from sportsApp.utils import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


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
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Add other fields as needed