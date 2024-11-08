# Generated by Django 4.2.16 on 2024-10-03 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0080_alter_goal_goal_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/teams/owner/')),
                ('descrption', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sportsApp.team')),
            ],
        ),
    ]