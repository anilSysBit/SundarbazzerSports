# Generated by Django 4.2.16 on 2024-09-11 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0068_alter_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(db_index=1, max_length=255),
        ),
    ]
