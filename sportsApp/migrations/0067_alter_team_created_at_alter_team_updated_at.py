# Generated by Django 4.2.16 on 2024-09-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0066_remove_team_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
