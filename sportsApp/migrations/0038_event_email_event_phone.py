# Generated by Django 4.2.7 on 2024-08-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0037_remove_event_email_remove_event_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]