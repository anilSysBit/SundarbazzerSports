# Generated by Django 4.2.16 on 2024-09-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0060_alter_eventorganizer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventorganizer',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]