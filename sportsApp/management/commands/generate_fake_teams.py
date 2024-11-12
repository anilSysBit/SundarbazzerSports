import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from sportsApp.models import Team
from sportsApp import constants  # Adjust based on your constants location

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake data for the Team model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Retrieve or create users if needed
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found. Please create some users first.'))
            return

        for _ in range(10):  # Number of teams to create
            user = random.choice(users)
            team = Team(
                name=fake.company(),
                total_players=random.randint(5, 20),
                short_name=fake.lexify(text="???").upper(),
                is_organizers_team=fake.boolean(),
                email=fake.email(),
                address=fake.address(),
                is_verified=fake.boolean(),
                user=user,
                logo=None,  # Add a default image or handle image uploads separately
                banner=None,
                gender=random.choice(constants.GENDER_OPTIONS.CHOICES)[0],
            )
            team.save()
            self.stdout.write(self.style.SUCCESS(f'Team "{team.name}" created.'))
