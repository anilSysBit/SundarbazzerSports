# Generated by Django 4.2.16 on 2024-11-11 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0004_alter_player_height_alter_player_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='resistration_end_date',
            new_name='registration_end_date',
        ),
    ]