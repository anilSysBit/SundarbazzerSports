# Generated by Django 4.2.16 on 2024-09-11 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0065_alter_match_team1_alter_match_team2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='email',
        ),
    ]