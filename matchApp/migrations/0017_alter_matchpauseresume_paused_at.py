# Generated by Django 4.2.16 on 2024-12-13 19:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matchApp', '0016_remove_matchpauseresume_match_time_manager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchpauseresume',
            name='paused_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The time when the match was paused.'),
        ),
    ]
