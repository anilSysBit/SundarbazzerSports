# Generated by Django 4.2.7 on 2024-08-22 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0034_rename_eventmembers_eventmember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
