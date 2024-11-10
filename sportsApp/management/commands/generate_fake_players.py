from django.core.management.base import BaseCommand
from faker import Faker
import random
from sportsApp.models import Player, Team  # Replace 'yourapp' with your actual app name
from sportsApp.constants import PLAYER_POSITION  # Import PLAYER_POSITION choices

class Command(BaseCommand):
    help = 'Generate fake players for specific teams'

    def add_arguments(self, parser):
        # Accept team_pks as a comma-separated list
        parser.add_argument(
            'team_pks',
            type=str,
            help='Comma-separated list of team primary keys to generate players for. Example: 16,17,19'
        )

    def handle(self, *args, **options):
        fake = Faker()
        # Parse the comma-separated team_pks argument
        team_pks = options['team_pks'].split(',')
        team_pks = [int(pk) for pk in team_pks]  # Convert to integers

        positions = [choice[0] for choice in PLAYER_POSITION.choices]

        for team_pk in team_pks:
            try:
                team = Team.objects.get(pk=team_pk)
                self.stdout.write(self.style.SUCCESS(f'Creating players for Team ID {team_pk}...'))
                
                for _ in range(11):
                    Player.objects.create(
                        team=team,
                        name=fake.name(),
                        jersey_no=random.randint(1, 99),
                        age=random.randint(18, 35),
                        email=fake.email(),
                        phone=fake.phone_number()[:10],
                        weight=random.randint(60, 90),
                        is_active=random.choice([True, False]),
                        height=random.randint(160, 200),
                        blood_group=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                        address=fake.address(),
                        designation=random.choice(positions),  # Use position choices
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully created 11 players for Team ID {team_pk}.'))
            except Team.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Team with ID {team_pk} does not exist.'))
        
        self.stdout.write(self.style.SUCCESS("Fake players created successfully!"))
