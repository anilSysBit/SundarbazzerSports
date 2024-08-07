# Generated by Django 4.2.7 on 2024-07-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsApp', '0007_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total_players', models.PositiveIntegerField(default=10)),
                ('sports_genere', models.CharField(choices=[('FOOTBALL', 'Football')], default='FOOTBALL', max_length=25)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_code',
        ),
        migrations.RemoveField(
            model_name='team',
            name='total_match_played',
        ),
        migrations.AddField(
            model_name='team',
            name='created_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='team',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='sports_genere',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='team',
            name='total_players',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('team', 'jersey_no'), name='unique_jersey_no_per_team'),
        ),
    ]
